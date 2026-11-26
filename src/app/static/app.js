/* ==========================================================================
   Interview Prep Viewer — frontend (vanilla JS, no build step)

   Sections:
     1. Utilities            5. Markdown rendering
     2. API client           6. Views: file page / dashboard / search
     3. Coverage store       7. Router + global events
     4. App state + sidebar

   Coverage ticks live ONLY in localStorage (key "prep.coverage.v1"), keyed
   by the stable question ids the backend generates.
   ========================================================================== */
"use strict";

(() => {
  // ------------------------------------------------------------------------
  // 1. Utilities
  // ------------------------------------------------------------------------
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const ESC = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ESC[c]);
  const pct = (done, total) => (total ? Math.round((done / total) * 100) : 0);
  const naturalCmp = new Intl.Collator(undefined, { numeric: true, sensitivity: "base" }).compare;

  /** Escape a title and turn `backticks` into <code>. */
  const inlineTitle = (t) => esc(t).replace(/`([^`]+)`/g, "<code>$1</code>");

  function stars(n, max = 3) {
    if (!n) return "";
    const total = Math.max(max, n);
    let out = "";
    for (let i = 1; i <= total; i++) out += i <= n ? "★" : '<span class="off">★</span>';
    return `<span class="stars" aria-label="Difficulty ${n} of ${total}" title="Difficulty ${n}/${total}">${out}</span>`;
  }

  function badgeClass(p) {
    return p >= 100 ? "badge done" : p > 0 ? "badge some" : "badge";
  }

  function timeAgo(ts) {
    const s = Math.round((Date.now() - ts) / 1000);
    if (s < 60) return "just now";
    const m = Math.round(s / 60);
    if (m < 60) return `${m}m ago`;
    const h = Math.round(m / 60);
    if (h < 24) return `${h}h ago`;
    return `${Math.round(h / 24)}d ago`;
  }

  let toastTimer;
  function toast(msg) {
    const el = $("#toast");
    el.textContent = msg;
    el.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => (el.hidden = true), 2600);
  }

  function debounce(fn, ms) {
    let t;
    return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), ms);
    };
  }

  // ------------------------------------------------------------------------
  // 2. API client
  // ------------------------------------------------------------------------
  const api = {
    async get(path, params = {}) {
      const url = new URL(path, location.origin);
      for (const [k, v] of Object.entries(params)) if (v != null) url.searchParams.set(k, v);
      const res = await fetch(url);
      if (!res.ok) throw new Error(`${res.status} ${(await res.json().catch(() => ({}))).detail || res.statusText}`);
      return res.json();
    },
    async post(path, body) {
      const res = await fetch(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: body ? JSON.stringify(body) : undefined,
      });
      if (!res.ok) throw new Error(`${res.status} ${(await res.json().catch(() => ({}))).detail || res.statusText}`);
      return res.json();
    },
  };

  // ------------------------------------------------------------------------
  // 3. Coverage store (localStorage only)
  // ------------------------------------------------------------------------
  const Coverage = (() => {
    const KEY = "prep.coverage.v1";
    const listeners = new Set();
    let data = read(); // { [questionId]: tickedAtMillis }

    function read() {
      try {
        const v = JSON.parse(localStorage.getItem(KEY) || "{}");
        return v && typeof v === "object" && !Array.isArray(v) ? v : {};
      } catch {
        return {};
      }
    }
    function save() {
      localStorage.setItem(KEY, JSON.stringify(data));
      listeners.forEach((fn) => fn());
    }
    // Keep several open tabs in sync.
    window.addEventListener("storage", (e) => {
      if (e.key === KEY) {
        data = read();
        listeners.forEach((fn) => fn());
      }
    });

    return {
      has: (id) => Object.prototype.hasOwnProperty.call(data, id),
      set(id, on) {
        if (on) data[id] = Date.now();
        else delete data[id];
        save();
      },
      setMany(ids, on) {
        const now = Date.now();
        for (const id of ids) {
          if (on) data[id] ??= now;
          else delete data[id];
        }
        save();
      },
      count: (ids) => ids.reduce((n, id) => n + (Object.prototype.hasOwnProperty.call(data, id) ? 1 : 0), 0),
      recent: (n) => Object.entries(data).sort((a, b) => b[1] - a[1]).slice(0, n),
      exportJSON: () => JSON.stringify({ version: 1, exported: new Date().toISOString(), coverage: data }, null, 2),
      importJSON(text) {
        const obj = JSON.parse(text);
        const incoming = obj && typeof obj.coverage === "object" ? obj.coverage : obj;
        let n = 0;
        for (const [id, ts] of Object.entries(incoming || {})) {
          if (typeof id === "string" && !(id in data)) {
            data[id] = Number(ts) || Date.now();
            n++;
          }
        }
        save();
        return n;
      },
      reset() {
        data = {};
        save();
      },
      onChange: (fn) => listeners.add(fn),
    };
  })();

  // ------------------------------------------------------------------------
  // 4. App state + sidebar
  // ------------------------------------------------------------------------
  const state = {
    topics: [], // TopicSummary[]
    stats: null, // Stats
    fileIds: new Map(), // "topic\u0000name" -> question ids
    byPath: new Map(), // repo-relative path -> { topic, name }
    summaries: new Map(), // topic | "*" -> QuestionSummary[] (search cache)
    route: { view: "dashboard" },
    current: null, // FileDetail currently on screen
    searchAll: false,
    renderToken: 0,
  };
  const main = $("#main");
  const sidebarInner = $("#sidebar-inner");
  const searchInput = $("#search");

  const fkey = (topic, name) => `${topic}\u0000${name}`;
  const idsForFile = (topic, name) => state.fileIds.get(fkey(topic, name)) || [];
  const idsForTopic = (topic) => {
    const t = state.topics.find((x) => x.name === topic);
    return t ? t.files.flatMap((f) => idsForFile(topic, f.name)) : [];
  };
  const allIds = () => Array.from(state.fileIds.values()).flat();

  const fileHref = (topic, name, anchor) =>
    `#/file/${encodeURIComponent(topic)}/${encodeURIComponent(name)}` + (anchor ? `/${encodeURIComponent(anchor)}` : "");

  async function loadData() {
    const [topics, stats] = await Promise.all([api.get("/api/topics"), api.get("/api/stats")]);
    state.topics = topics;
    state.stats = stats;
    state.fileIds = new Map(stats.files.map((f) => [fkey(f.topic, f.name), f.question_ids]));
    state.byPath = new Map(topics.flatMap((t) => t.files.map((f) => [f.path, { topic: f.topic, name: f.name }])));
    state.summaries.clear();
  }

  const OPEN_KEY = "prep.openTopics";
  const openTopics = new Set(JSON.parse(localStorage.getItem(OPEN_KEY) || "[]"));

  function renderSidebar() {
    const r = state.route;
    if (r.view === "file") openTopics.add(r.topic);
    const all = allIds();
    const overall = pct(Coverage.count(all), all.length);

    let html = `
      <a class="nav-link ${r.view === "dashboard" ? "active" : ""}" href="#/">
        <span aria-hidden="true">◎</span><span class="topic-name">Dashboard</span>
        <span class="${badgeClass(overall)}" data-badge="all">${overall}%</span>
      </a>
      <div class="nav-heading">Topics · ${state.topics.length}</div>`;

    for (const t of state.topics) {
      const tp = pct(Coverage.count(idsForTopic(t.name)), t.question_count);
      html += `
        <details class="topic" data-topic="${esc(t.name)}" ${openTopics.has(t.name) ? "open" : ""}>
          <summary>
            <span class="chev" aria-hidden="true">▶</span>
            <span class="topic-name" title="${esc(t.name)}">${esc(t.name)}</span>
            <span class="count" title="${t.question_count} questions">${t.question_count}</span>
            <span class="${badgeClass(tp)}" data-badge-topic="${esc(t.name)}">${tp}%</span>
          </summary>
          <ul class="topic-files">`;
      for (const f of t.files) {
        const active = r.view === "file" && r.topic === t.name && r.file === f.name;
        const fp = pct(Coverage.count(idsForFile(t.name, f.name)), f.question_count);
        html += `
            <li><a class="file-link ${active ? "active" : ""}" href="${fileHref(t.name, f.name)}"
                   ${active ? 'aria-current="page"' : ""} title="${esc(f.title)}">
              <span class="file-label">${esc(f.label)}</span>
              <span class="count">${f.format === "document" ? "doc" : f.question_count}</span>
              <span class="${badgeClass(fp)}" data-badge-file="${esc(fkey(t.name, f.name))}">${fp}%</span>
            </a></li>`;
      }
      html += `</ul></details>`;
    }
    sidebarInner.innerHTML = html;
    $(".file-link.active", sidebarInner)?.scrollIntoView({ block: "nearest" });
  }

  /** Cheap in-place update of the sidebar % badges after a tick. */
  function updateSidebarBadges() {
    const setBadge = (el, p) => {
      if (!el) return;
      el.textContent = `${p}%`;
      el.className = badgeClass(p);
    };
    const all = allIds();
    setBadge($('[data-badge="all"]', sidebarInner), pct(Coverage.count(all), all.length));
    for (const el of $$("[data-badge-topic]", sidebarInner)) {
      const ids = idsForTopic(el.dataset.badgeTopic);
      setBadge(el, pct(Coverage.count(ids), ids.length));
    }
    for (const el of $$("[data-badge-file]", sidebarInner)) {
      const ids = state.fileIds.get(el.dataset.badgeFile) || [];
      setBadge(el, pct(Coverage.count(ids), ids.length));
    }
  }

  // Remember which topics are expanded (toggle doesn't bubble → capture).
  sidebarInner.addEventListener(
    "toggle",
    (e) => {
      const d = e.target;
      if (!d.matches?.("details.topic")) return;
      d.open ? openTopics.add(d.dataset.topic) : openTopics.delete(d.dataset.topic);
      localStorage.setItem(OPEN_KEY, JSON.stringify([...openTopics]));
    },
    true
  );

  // ------------------------------------------------------------------------
  // 5. Markdown rendering
  // ------------------------------------------------------------------------
  if (window.marked) marked.setOptions({ gfm: true, breaks: false });

  // Highlight code blocks only when they scroll near the viewport — keeps
  // 160 KB ORM modules snappy.
  const highlighter =
    "IntersectionObserver" in window
      ? new IntersectionObserver(
          (entries) => {
            for (const e of entries) {
              if (!e.isIntersecting) continue;
              highlighter.unobserve(e.target);
              highlightCode(e.target);
            }
          },
          { rootMargin: "800px 0px" }
        )
      : null;

  function highlightCode(code) {
    if (!window.hljs || code.dataset.highlighted) return;
    const lang = (code.className.match(/language-([\w+#.-]+)/) || [])[1];
    if (lang && !hljs.getLanguage(lang)) return; // unknown language → leave plain
    hljs.highlightElement(code);
  }

  function renderMarkdown(el, md, file) {
    el.innerHTML = window.marked ? marked.parse(md || "") : `<pre><code>${esc(md)}</code></pre>`;
    el.classList.add("md");
    for (const code of $$("pre > code", el)) {
      const lang = (code.className.match(/language-([\w+#.-]+)/) || [])[1];
      if (lang) {
        const tag = document.createElement("span");
        tag.className = "lang";
        tag.textContent = lang;
        code.parentElement.appendChild(tag);
      }
      highlighter ? highlighter.observe(code) : highlightCode(code);
    }
    for (const a of $$("a[href]", el)) rewriteLink(a, file);
  }

  const ghSlug = (s) =>
    s.toLowerCase().trim().replace(/[^\p{L}\p{N}\s-]/gu, "").replace(/\s/g, "-");
  const looseText = (s) =>
    s.replace(/\[([^\]]*)\]\([^)]*\)/g, "$1").toLowerCase().replace(/[^\p{L}\p{N}]+/gu, "");

  function dirname(p) {
    const i = p.lastIndexOf("/");
    return i < 0 ? "" : p.slice(0, i);
  }
  function joinPath(base, rel) {
    const out = base ? base.split("/") : [];
    for (const part of rel.split("/")) {
      if (part === "" || part === ".") continue;
      if (part === "..") out.pop();
      else out.push(part);
    }
    return out.join("/");
  }

  /** Map an in-file "#fragment" to one of our DOM anchors (or null). */
  function resolveFragment(frag, file) {
    if (!frag || !file) return null;
    frag = decodeURIComponent(frag).toLowerCase();
    const qm = frag.match(/^q(\d+)\b/);
    if (qm && file.format !== "document") {
      const q = file.questions.find((x) => x.index === Number(qm[1]));
      if (q) return q.anchor;
    }
    const t = file.toc.find((x) => ghSlug(x.title) === frag);
    if (t) return t.anchor;
    const q = file.questions.find((x) => ghSlug(x.title) === frag);
    return q ? q.anchor : null;
  }

  /** Keep links working inside the single-page app. */
  function rewriteLink(a, file) {
    const href = a.getAttribute("href");
    if (/^[a-z][a-z0-9+.-]*:/i.test(href)) {
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      return;
    }
    const [pathPart, frag] = href.split("#");
    if (!pathPart) {
      // "#something" inside this file. Hash routing owns location.hash, so
      // translate it into a route (falls back to the top of the file).
      if (file) a.setAttribute("href", fileHref(file.topic, file.name, resolveFragment(frag, file)));
      return;
    }
    if (file && /\.md$/i.test(pathPart)) {
      let target;
      try {
        target = joinPath(dirname(file.path), decodeURIComponent(pathPart));
      } catch {
        target = joinPath(dirname(file.path), pathPart);
      }
      const hit = state.byPath.get(target);
      if (hit) {
        a.setAttribute("href", fileHref(hit.topic, hit.name));
        return;
      }
    }
    // Something we can't show (meta file, .py, …): make it inert.
    a.removeAttribute("href");
    a.title = `Not available in the viewer: ${href}`;
    a.style.cursor = "help";
  }

  // ------------------------------------------------------------------------
  // 6a. View: file page
  // ------------------------------------------------------------------------
  const FORMAT_LABEL = { deep: "Deep answers", compact: "Q&A", document: "Document" };

  async function renderFile(topic, name, anchor) {
    const token = ++state.renderToken;
    main.innerHTML = `<div class="loading">Loading ${esc(name)}…</div>`;
    let f;
    try {
      f = await api.get("/api/file", { topic, file: name });
    } catch (err) {
      if (token !== state.renderToken) return;
      main.innerHTML = `<div class="card error-box"><strong>Could not load this file.</strong><br>${esc(err.message)}
        <p><a href="#/">← Back to dashboard</a></p></div>`;
      return;
    }
    if (token !== state.renderToken) return; // user navigated away meanwhile
    state.current = f;
    document.title = `${f.label} · ${f.topic} — Interview Prep`;

    const isDoc = f.format === "document";
    const notesAfter = new Map();
    for (const n of f.notes) {
      if (!notesAfter.has(n.after)) notesAfter.set(n.after, []);
      notesAfter.get(n.after).push(n);
    }

    // Intro: drop the H1 that duplicates the page title.
    const intro = (f.intro_markdown || "").replace(/^#\s+.*\n?/, "").trim();

    let html = `
      <div data-file-page>
        <header class="page-head">
          <div class="crumbs"><a href="#/">Dashboard</a> / <span>${esc(f.topic)}</span> / <span>${esc(f.name)}</span></div>
          <h1 class="page-title">${inlineTitle(f.title)}</h1>
          <div class="page-meta">
            <span class="pill">${FORMAT_LABEL[f.format]}</span>
            ${isDoc ? `<span>${f.toc.length} sections</span>` : `<span>${f.questions.length} questions</span>`}
            <div class="progress" id="file-progress" aria-hidden="true"><span style="width:0"></span></div>
            <span id="file-progress-text"></span>
            <span class="spacer"></span>
            <button class="btn" id="file-done-btn" type="button"></button>
          </div>
          ${f.error ? `<div class="card error-box" style="margin-top:12px">⚠️ Shown as a plain document: ${esc(f.error)}</div>` : ""}
        </header>`;

    if (intro) {
      html += `<details class="card intro"><summary>About this file</summary><div data-intro></div></details>`;
    }

    // ---- Short index (questions) or table of contents (documents) ----
    if (isDoc) {
      html += `<section class="card qindex toc" id="qindex" aria-label="Table of contents">
        <div class="qindex-head"><h2>Contents</h2></div>
        ${f.toc.length ? `<ol>${f.toc
          .map((t) => `<li><a href="${fileHref(f.topic, f.name, t.anchor)}" style="--indent:${(t.level - 1) * 16}px">
              <span class="qtitle">${inlineTitle(t.title)}</span></a></li>`)
          .join("")}</ol>` : `<div class="empty">No headings in this file.</div>`}
      </section>`;
    } else {
      html += `<section class="card qindex" id="qindex" aria-label="Question index">
        <div class="qindex-head">
          <h2>Question index</h2>
          <input class="qindex-filter" id="qindex-filter" type="search" placeholder="Filter this file…" aria-label="Filter questions in this file" />
          <span class="count" id="qindex-count"></span>
        </div>
        <div id="qindex-list">${renderIndexGroups(f, notesAfter)}</div>
      </section>`;
    }

    // ---- Full question cards ----
    html += `<div id="qlist">`;
    for (const n of notesAfter.get(0) || []) html += noteCard(n);
    f.questions.forEach((q, i) => {
      html += questionCard(q, f, i);
      for (const n of notesAfter.get(i + 1) || []) html += noteCard(n);
    });
    html += `</div></div>
      <button class="btn back-top" id="back-top" type="button" title="Back to the index">↑ Index</button>`;

    main.innerHTML = html;

    // Render markdown into the placeholders.
    if (intro) renderMarkdown($("[data-intro]", main), intro, f);
    f.questions.forEach((q, i) => renderMarkdown($(`[data-md-q="${i}"]`, main), q.markdown, f));
    f.notes.forEach((n, i) => renderMarkdown($(`[data-md-note="${i}"]`, main), n.markdown, f));
    if (isDoc) assignDocHeadingIds($('[data-md-q="0"]', main), f.toc);

    updateFilePage();
    requestAnimationFrame(() => scrollToAnchor(anchor));
  }

  function renderIndexGroups(f, notesAfter) {
    const groups = [];
    let cur = null;
    const push = (section, li) => {
      if (!cur || cur.section !== section) groups.push((cur = { section, items: [] }));
      cur.items.push(li);
    };
    f.questions.forEach((q, i) => {
      push(q.section, `<li data-qid="${esc(q.id)}" data-title="${esc(q.title.toLowerCase())}">
        <a href="${fileHref(f.topic, f.name, q.anchor)}">
          <span class="tick" aria-hidden="true">✓</span>
          <span class="qnum">${q.index}.</span>
          <span class="qtitle">${inlineTitle(q.title)}</span>
          ${stars(q.difficulty)}
        </a></li>`);
      for (const n of notesAfter.get(i + 1) || []) {
        push(q.section, `<li data-title="${esc(n.title.toLowerCase())}">
          <a href="${fileHref(f.topic, f.name, n.anchor)}">
            <span class="tick" aria-hidden="true" style="border-style:dashed"></span>
            <span class="qnum">📎</span><span class="qtitle">${inlineTitle(n.title)}</span>
          </a></li>`);
      }
    });
    return groups
      .map(
        (g) => `<div class="qgroup">
          ${g.section ? `<div class="qindex-section">${esc(g.section)}</div>` : ""}
          <ol>${g.items.join("")}</ol></div>`
      )
      .join("");
  }

  function questionCard(q, f, i) {
    const isDoc = f.format === "document";
    return `
      <article class="card qcard" id="${esc(q.anchor)}" data-qid="${esc(q.id)}">
        <header class="qcard-head">
          <label class="check" title="${isDoc ? "Mark document as read" : "Mark as covered"}">
            <input type="checkbox" data-check="${esc(q.id)}"
                   aria-label="${isDoc ? "Mark document as read" : `Mark question ${q.index} as covered`}" />
            <span class="box" aria-hidden="true">✓</span>
          </label>
          <div class="qcard-title">
            <h2>${inlineTitle(isDoc ? "Full document" : q.title)}</h2>
            <div class="qcard-meta">
              ${isDoc ? "<span>Tick when you've read it</span>" : `<span>Q${q.index}</span>${stars(q.difficulty)}`}
              ${q.section ? `<span>· ${esc(q.section)}</span>` : ""}
            </div>
          </div>
          <div class="qcard-actions">
            <!-- FUTURE HOOK: comments. Will POST /api/comment {question_id, text}.
                 Disabled until the backend can append to the markdown file. -->
            <button class="btn small ghost" type="button" disabled aria-disabled="true"
                    data-comment="${esc(q.id)}" title="Coming soon — comments will be saved back into the markdown file">💬 Comment</button>
            <button class="btn small ghost" type="button" data-copy="${esc(q.anchor)}" title="Copy link to this question" aria-label="Copy link">🔗</button>
            <button class="btn small ghost" type="button" data-to-index title="Back to the index" aria-label="Back to the index">↑</button>
          </div>
        </header>
        <div class="qcard-body" data-md-q="${i}"></div>
      </article>`;
  }

  function noteCard(n) {
    const i = state.current ? state.current.notes.indexOf(n) : 0;
    return `
      <article class="card qcard note-card" id="${esc(n.anchor)}">
        <header class="qcard-head">
          <div class="qcard-title"><h2>📎 ${inlineTitle(n.title)}</h2>
            <div class="qcard-meta"><span>Extra notes from this file · not counted for coverage</span></div></div>
        </header>
        <div class="qcard-body" data-md-note="${i}"></div>
      </article>`;
  }

  /** Give rendered document headings the ids the backend's TOC points at. */
  function assignDocHeadingIds(container, toc) {
    if (!container) return;
    let j = 0;
    for (const h of $$("h1, h2, h3", container)) {
      const text = looseText(h.textContent);
      for (let k = j; k < Math.min(j + 4, toc.length); k++) {
        if (looseText(toc[k].title) === text) {
          h.id = toc[k].anchor;
          h.style.scrollMarginTop = "calc(var(--topbar-h) + 14px)";
          j = k + 1;
          break;
        }
      }
    }
  }

  /** Sync checkboxes, card states, index ticks and the file progress bar. */
  function updateFilePage() {
    const f = state.current;
    if (!f || !$("[data-file-page]", main)) return;
    const ids = f.questions.map((q) => q.id);
    const done = Coverage.count(ids);
    const p = pct(done, ids.length);

    for (const box of $$("[data-check]", main)) box.checked = Coverage.has(box.dataset.check);
    for (const card of $$(".qcard[data-qid]", main)) card.classList.toggle("covered", Coverage.has(card.dataset.qid));
    for (const li of $$("#qindex-list li[data-qid]", main)) li.classList.toggle("covered", Coverage.has(li.dataset.qid));

    const bar = $("#file-progress", main);
    bar.classList.toggle("done", p >= 100);
    $("span", bar).style.width = `${p}%`;
    $("#file-progress-text", main).textContent = `${done}/${ids.length} covered · ${p}%`;

    const btn = $("#file-done-btn", main);
    const all = done === ids.length && ids.length > 0;
    btn.textContent = all ? "↺ Unmark file" : f.format === "document" ? "✓ Mark as read" : "✓ Mark file done";
    btn.className = all ? "btn success" : "btn primary";
  }

  function scrollToAnchor(anchor) {
    if (!anchor) {
      window.scrollTo({ top: 0 });
      return;
    }
    const el = document.getElementById(anchor);
    if (!el) return;
    el.scrollIntoView({ block: "start" });
    el.classList.add("flash");
    setTimeout(() => el.classList.remove("flash"), 1400);
  }

  // Delegated events on the main pane.
  main.addEventListener("change", (e) => {
    const box = e.target.closest("[data-check]");
    if (box) Coverage.set(box.dataset.check, box.checked);
  });

  main.addEventListener("click", (e) => {
    const t = e.target;
    if (t.closest("#file-done-btn") && state.current) {
      const ids = state.current.questions.map((q) => q.id);
      const all = Coverage.count(ids) === ids.length;
      Coverage.setMany(ids, !all);
      toast(all ? "File unmarked" : `Marked ${ids.length} as covered 🎉`);
    } else if (t.closest("[data-to-index]") || t.closest("#back-top")) {
      $("#qindex")?.scrollIntoView({ block: "start" });
      if (state.current) history.replaceState(null, "", fileHref(state.current.topic, state.current.name));
    } else if (t.closest("[data-copy]") && state.current) {
      const a = t.closest("[data-copy]").dataset.copy;
      const url = `${location.origin}/${fileHref(state.current.topic, state.current.name, a)}`;
      navigator.clipboard?.writeText(url).then(() => toast("Link copied"), () => toast(url));
    } else if (t.closest("[data-more]")) {
      const card = t.closest(".topic-card");
      $$(".extra", card).forEach((li) => (li.hidden = !li.hidden));
      const btn = t.closest("[data-more]");
      btn.textContent = btn.textContent.startsWith("Show") ? "Show less" : btn.dataset.more;
    }
  });

  main.addEventListener("input", (e) => {
    if (e.target.id !== "qindex-filter") return;
    const q = e.target.value.trim().toLowerCase();
    let shown = 0;
    for (const g of $$(".qgroup", main)) {
      let groupShown = 0;
      for (const li of $$("li", g)) {
        const ok = !q || li.dataset.title.includes(q);
        li.hidden = !ok;
        if (ok) groupShown++;
      }
      g.hidden = groupShown === 0;
      shown += groupShown;
    }
    $("#qindex-count", main).textContent = q ? `${shown} match${shown === 1 ? "" : "es"}` : "";
  });

  // ------------------------------------------------------------------------
  // 6b. View: dashboard
  // ------------------------------------------------------------------------
  function ring(p, size, stroke, sub) {
    const r = (size - stroke) / 2;
    const c = 2 * Math.PI * r;
    const half = size / 2;
    return `
      <svg class="ring ${p >= 100 ? "done" : ""}" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}"
           role="img" aria-label="${p}% covered">
        <circle class="track" cx="${half}" cy="${half}" r="${r}" fill="none" stroke-width="${stroke}" />
        <circle class="bar" cx="${half}" cy="${half}" r="${r}" fill="none" stroke-width="${stroke}"
                stroke-linecap="round" stroke-dasharray="${c}" stroke-dashoffset="${c}"
                data-target="${c * (1 - p / 100)}" transform="rotate(-90 ${half} ${half})" />
        <text x="50%" y="${sub ? "47%" : "50%"}" text-anchor="middle" dominant-baseline="middle"
              font-size="${Math.round(size * 0.22)}">${p}%</text>
        ${sub ? `<text class="sub" x="50%" y="66%" text-anchor="middle" font-size="${Math.round(size * 0.085)}">${esc(sub)}</text>` : ""}
      </svg>`;
  }

  function renderDashboard() {
    state.current = null;
    document.title = "Dashboard — Interview Prep";
    const all = allIds();
    const done = Coverage.count(all);
    const p = pct(done, all.length);
    let filesDone = 0;
    for (const ids of state.fileIds.values()) if (ids.length && Coverage.count(ids) === ids.length) filesDone++;
    const s = state.stats;

    const greeting =
      p === 0 ? "Pick a topic on the left and start ticking questions."
      : p < 25 ? "Good start — keep the streak going."
      : p < 60 ? "Solid progress. You're building real depth."
      : p < 100 ? "Home stretch. Polish the hard ones."
      : "Everything covered. Time for mock interviews! 🎉";

    let html = `
      <section class="card hero">
        ${ring(p, 168, 14, "covered")}
        <div>
          <h1>Your prep progress</h1>
          <p><strong>${done.toLocaleString()}</strong> of <strong>${all.length.toLocaleString()}</strong> questions covered. ${greeting}</p>
          <div class="hero-actions">
            <button class="btn" type="button" id="export-btn">⇩ Export progress</button>
            <button class="btn" type="button" id="import-btn">⇧ Import progress</button>
            <button class="btn ghost" type="button" id="reset-btn">Reset</button>
            <input type="file" id="import-file" accept="application/json,.json" hidden />
          </div>
        </div>
      </section>

      <div class="tiles">
        <div class="card tile"><div class="k">Topics</div><div class="v">${s.topic_count}</div></div>
        <div class="card tile"><div class="k">Files</div><div class="v">${s.file_count}</div></div>
        <div class="card tile"><div class="k">Questions</div><div class="v">${s.question_count.toLocaleString()}</div></div>
        <div class="card tile"><div class="k">Covered</div><div class="v">${done.toLocaleString()} <small>${p}%</small></div></div>
        <div class="card tile"><div class="k">Files done</div><div class="v">${filesDone} <small>/ ${s.file_count}</small></div></div>
      </div>

      <h2 class="section-title">By topic</h2>
      <div class="topic-grid">`;

    for (const t of state.topics) {
      const tids = idsForTopic(t.name);
      const td = Coverage.count(tids);
      const tp = pct(td, tids.length);
      const LIMIT = 6;
      html += `
        <section class="card topic-card">
          <div class="topic-card-head">
            ${ring(tp, 64, 7)}
            <div><h3>${esc(t.name)}</h3>
              <div class="sub">${td} / ${tids.length} covered · ${t.file_count} file${t.file_count === 1 ? "" : "s"}</div></div>
          </div>
          <ul class="file-bars">
            ${t.files
              .map((f, i) => {
                const ids = idsForFile(t.name, f.name);
                const d = Coverage.count(ids);
                const fp = pct(d, ids.length);
                return `<li class="${i >= LIMIT ? "extra" : ""}" ${i >= LIMIT ? "hidden" : ""}>
                  <a href="${fileHref(t.name, f.name)}" title="${esc(f.title)}">
                    <span class="fname">${esc(f.label)}</span>
                    <span class="progress ${fp >= 100 ? "done" : ""}"><span style="width:${fp}%"></span></span>
                    <span class="fcount">${d}/${ids.length}</span>
                  </a></li>`;
              })
              .join("")}
          </ul>
          ${t.files.length > LIMIT
            ? `<button class="btn small ghost more-btn" type="button" data-more="Show all ${t.files.length} files">Show all ${t.files.length} files</button>`
            : ""}
        </section>`;
    }
    html += `</div>
      <h2 class="section-title">Recently covered</h2>
      <section class="card recent" id="recent"><div class="empty-state" style="padding:20px">Nothing ticked yet.</div></section>`;

    main.innerHTML = html;

    // Animate rings from 0 to their value.
    requestAnimationFrame(() =>
      requestAnimationFrame(() => {
        for (const c of $$(".ring .bar", main)) c.style.strokeDashoffset = c.dataset.target;
      })
    );
    fillRecent();
  }

  async function fillRecent() {
    const recent = Coverage.recent(8);
    if (!recent.length) return;
    const list = await getSummaries(null).catch(() => []);
    const byId = new Map(list.map((q) => [q.id, q]));
    const items = recent.map(([id, ts]) => [byId.get(id), ts]).filter(([q]) => q);
    const box = $("#recent", main);
    if (!box || !items.length) return;
    box.innerHTML = `<ul>${items
      .map(
        ([q, ts]) => `<li><a href="${fileHref(q.topic, q.file, q.anchor)}">
          <span class="what">${inlineTitle(q.title)}</span>
          <span class="where">${esc(q.topic)} · ${esc(q.file.replace(/\.md$/i, ""))}</span>
          <span class="when">${timeAgo(ts)}</span></a></li>`
      )
      .join("")}</ul>`;
  }

  // Dashboard buttons (export / import / reset).
  main.addEventListener("click", (e) => {
    if (e.target.closest("#export-btn")) {
      const blob = new Blob([Coverage.exportJSON()], { type: "application/json" });
      const a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `interview-prep-progress-${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      URL.revokeObjectURL(a.href);
    } else if (e.target.closest("#import-btn")) {
      $("#import-file", main).click();
    } else if (e.target.closest("#reset-btn")) {
      if (confirm("Clear ALL coverage ticks stored in this browser?")) {
        Coverage.reset();
        toast("Progress reset");
      }
    }
  });
  main.addEventListener("change", async (e) => {
    if (e.target.id !== "import-file" || !e.target.files[0]) return;
    try {
      const n = Coverage.importJSON(await e.target.files[0].text());
      toast(`Imported ${n} new tick${n === 1 ? "" : "s"}`);
    } catch {
      toast("That file isn't a valid progress export");
    }
  });

  // ------------------------------------------------------------------------
  // 6c. View: search results
  // ------------------------------------------------------------------------
  async function getSummaries(topic) {
    const key = topic ?? "*";
    if (!state.summaries.has(key)) {
      state.summaries.set(key, await api.get("/api/questions", topic ? { topic } : {}));
    }
    return state.summaries.get(key);
  }

  function highlight(text, terms) {
    if (!terms.length) return esc(text);
    const re = new RegExp(`(${terms.map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})`, "gi");
    return text
      .split(re)
      .map((part, i) => (i % 2 ? `<mark>${esc(part)}</mark>` : esc(part)))
      .join("");
  }

  async function renderSearch(query) {
    const token = ++state.renderToken;
    const r = state.route;
    const scope = r.view === "file" && !state.searchAll ? r.topic : null;
    let list;
    try {
      list = await getSummaries(scope);
    } catch (err) {
      main.innerHTML = `<div class="card error-box">${esc(err.message)}</div>`;
      return;
    }
    if (token !== state.renderToken) return;

    const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    const hits = list.filter((q) => {
      const t = q.title.toLowerCase();
      return terms.every((term) => t.includes(term));
    });

    const groups = new Map();
    for (const q of hits.slice(0, 400)) {
      const k = fkey(q.topic, q.file);
      if (!groups.has(k)) groups.set(k, []);
      groups.get(k).push(q);
    }

    let html = `
      <div class="results-head">
        <h1>${hits.length} result${hits.length === 1 ? "" : "s"}</h1>
        <span class="count">for “${esc(query)}” in ${scope ? esc(scope) : "all topics"}</span>
        <span class="spacer"></span>
        ${r.view === "file"
          ? `<button class="btn small" type="button" id="scope-btn">${scope ? "Search all topics" : `Only ${esc(r.topic)}`}</button>`
          : ""}
      </div>`;
    if (!hits.length) {
      html += `<div class="empty-state"><div class="big">🔍</div><p>No question titles match. Try fewer words.</p></div>`;
    }
    for (const qs of groups.values()) {
      const q0 = qs[0];
      html += `<section class="card result-group"><h3>${esc(q0.topic)} · ${esc(q0.file.replace(/\.md$/i, ""))}</h3>
        ${qs
          .map(
            (q) => `<a href="${fileHref(q.topic, q.file, q.anchor)}" data-result>
              <span class="tick" aria-hidden="true">${Coverage.has(q.id) ? "✅" : "▫️"}</span>
              <span class="qtitle">${highlight(q.title.replace(/`/g, ""), terms)}</span>${stars(q.difficulty)}</a>`
          )
          .join("")}
      </section>`;
    }
    main.innerHTML = html;
  }

  main.addEventListener("click", (e) => {
    if (e.target.closest("#scope-btn")) {
      state.searchAll = !state.searchAll;
      renderSearch(searchInput.value.trim());
      return;
    }
    const res = e.target.closest("[data-result]");
    if (res) {
      e.preventDefault();
      searchInput.value = "";
      navigate(res.getAttribute("href"));
    }
  });

  const onSearch = debounce(() => {
    const q = searchInput.value.trim();
    if (q) renderSearch(q);
    else {
      state.searchAll = false;
      route(true);
    }
  }, 120);
  searchInput.addEventListener("input", onSearch);
  searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      searchInput.value = "";
      onSearch();
      searchInput.blur();
    } else if (e.key === "Enter") {
      const first = $("[data-result]", main);
      if (first) first.click();
    }
  });

  // ------------------------------------------------------------------------
  // 7. Router + global events
  // ------------------------------------------------------------------------
  function parseRoute() {
    const parts = location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
    const dec = (s) => {
      try {
        return decodeURIComponent(s);
      } catch {
        return s;
      }
    };
    if (parts[0] === "file" && parts.length >= 3) {
      return { view: "file", topic: dec(parts[1]), file: dec(parts[2]), anchor: parts[3] ? dec(parts[3]) : null };
    }
    return { view: "dashboard" };
  }

  function navigate(href) {
    if (location.hash === href) route(true);
    else location.hash = href;
  }

  async function route(force = false) {
    const r = parseRoute();
    const prev = state.route;
    state.route = r;
    closeSidebar();
    if (searchInput.value.trim() && !force) searchInput.value = "";

    if (r.view === "file") {
      const same =
        !force && state.current && state.current.topic === r.topic && state.current.name === r.file && $("[data-file-page]", main);
      if (same) scrollToAnchor(r.anchor);
      else await renderFile(r.topic, r.file, r.anchor);
    } else {
      ++state.renderToken;
      renderDashboard();
      window.scrollTo({ top: 0 });
    }
    const sidebarChanged = prev.view !== r.view || prev.topic !== r.topic || prev.file !== r.file;
    if (sidebarChanged || force || !sidebarInner.querySelector(".nav-link")) renderSidebar();
  }

  window.addEventListener("hashchange", () => route());

  // Coverage changed (this tab or another): refresh what's on screen.
  Coverage.onChange(() => {
    updateSidebarBadges();
    if (searchInput.value.trim()) return;
    if (state.route.view === "file") updateFilePage();
    else renderDashboard();
  });

  // Theme
  function applyHljsTheme() {
    const dark = document.documentElement.dataset.theme === "dark";
    $("#hljs-light").disabled = dark;
    $("#hljs-dark").disabled = !dark;
  }
  $("#theme-btn").addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    localStorage.setItem("prep.theme", next);
    applyHljsTheme();
  });
  applyHljsTheme();

  // Rescan
  $("#rescan-btn").addEventListener("click", async () => {
    const btn = $("#rescan-btn");
    btn.classList.add("spinning");
    try {
      const r = await api.post("/api/rescan");
      await loadData();
      state.current = null;
      await route(true);
      toast(`Rescanned ${r.file_count} files · ${r.question_count} questions (${r.seconds}s)`);
    } catch (err) {
      toast(`Rescan failed: ${err.message}`);
    } finally {
      btn.classList.remove("spinning");
    }
  });

  // Mobile sidebar
  const sidebar = $("#sidebar");
  const scrim = $("#scrim");
  const menuBtn = $("#menu-btn");
  function closeSidebar() {
    sidebar.classList.remove("open");
    scrim.hidden = true;
    menuBtn.setAttribute("aria-expanded", "false");
  }
  menuBtn.addEventListener("click", () => {
    const open = !sidebar.classList.contains("open");
    sidebar.classList.toggle("open", open);
    scrim.hidden = !open;
    menuBtn.setAttribute("aria-expanded", String(open));
  });
  scrim.addEventListener("click", closeSidebar);

  // "/" focuses search
  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) {
      e.preventDefault();
      searchInput.focus();
      searchInput.select();
    }
  });

  // Boot
  (async function boot() {
    if (!window.marked) console.warn("marked failed to load — showing raw markdown. See README (offline).");
    try {
      await loadData();
    } catch (err) {
      main.innerHTML = `<div class="card error-box"><strong>Could not reach the API.</strong><br>${esc(err.message)}</div>`;
      sidebarInner.innerHTML = "";
      return;
    }
    await route(true);
  })();
})();
