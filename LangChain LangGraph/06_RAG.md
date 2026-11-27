# RAG (Retrieval-Augmented Generation)
### [← LangChain & LangGraph index](./README.md) · [Question Bank](./Question_Bank.md)

Twenty questions on retrieval-augmented generation. This is your strongest area because FinSight gives you real numbers (99% correct filing, 61% gold page in the top 10 on FinanceBench), so steer conversations here.

**How to use each answer:** say the **Answer** (20–30 seconds) first. Use **How it works**, the **Formula** and the **Example** only when the interviewer digs deeper. Code is LangChain 1.x. Legacy retrievers (`EnsembleRetriever`, `ContextualCompressionRetriever`, `MultiQueryRetriever`, `ParentDocumentRetriever`, `SQLRecordManager`) now live in `langchain-classic`. In 0.3 they were imported from `langchain.retrievers` / `langchain.indexes`.

**Topics:** [Fundamentals](./01_LangChain_Fundamentals.md) · [LCEL](./02_LCEL_and_Runnables.md) · [Prompts](./03_Prompts.md) · [Models](./04_Models_and_Structured_Output.md) · [Memory](./05_Memory_and_Chat_History.md) · [RAG](./06_RAG.md) · [Tools & Agents](./07_Tools_and_Agents.md) · [LangGraph](./08_LangGraph_Core.md) · [Checkpointing](./09_Checkpointing_and_HITL.md) · [Multi-agent](./10_Multi_Agent_Systems.md) · [Streaming](./11_Streaming_and_Async.md) · [LangSmith](./12_LangSmith_and_Evaluation.md) · [Production](./13_Production_and_Django.md) · [System Design](./14_System_Design.md)

## Formula cheat sheet

| What | Formula | Typical value |
|---|---|---|
| Cosine similarity | `cos(q, d) = (q · d) / (‖q‖ · ‖d‖)` | −1 to 1; equals the dot product when vectors are normalised |
| Number of chunks | `n ≈ ceil((L − O) / (C − O))` | L = doc length, C = chunk size, O = overlap |
| Vector storage | `n_vectors × dim × 4 bytes` (float32) | 1M × 768 × 4 ≈ 3.1 GB |
| BM25 | `Σ IDF(t) · f(t,D)(k1+1) / (f(t,D) + k1(1 − b + b·|D|/avgdl))` | k1 = 1.2–2.0, b = 0.75 |
| RRF | `score(d) = Σ_lists 1 / (k + rank(d))` | k = 60 |
| Recall@k / Hit rate@k | `relevant in top k / total relevant`; hit = at least 1 relevant in top k | your 61% is hit rate@10 on gold pages |
| MRR | `(1/|Q|) Σ 1 / rank_of_first_relevant` | 1.0 = always first |
| nDCG@k | `DCG / IDCG`, `DCG = Σ rel_i / log2(i + 1)` | 0 to 1 |
| Faithfulness (RAGAS) | `claims supported by context / total claims in answer` | aim > 0.9 |
| Prompt tokens per query | `system + question + k × chunk_tokens` | 5 × 500 + 300 ≈ 2.8k |

## Table of Contents

1. (Easy) [Explain RAG end to end.](#q1)
2. (Easy) [Why RAG instead of fine-tuning?](#q2)
3. (Easy) [How do you choose a chunking strategy and chunk size?](#q3)
4. (Easy) [What is chunk overlap and why use it?](#q4)
5. (Easy) [How do vector databases search? What is ANN and HNSW?](#q5)
6. (Easy) [How do you choose a vector store?](#q6)
7. (Medium) [What is hybrid search?](#q7)
8. (Medium) [What is Reciprocal Rank Fusion?](#q8)
9. (Medium) [What is reranking?](#q9)
10. (Medium) [Bi-encoder versus cross-encoder?](#q10)
11. (Medium) [How do you evaluate a RAG system?](#q11)
12. (Medium) [Why is your top-10 page retrieval only 61%?](#q12)
13. (Medium) [What advanced retrieval techniques do you know?](#q13)
14. (Medium) [What is agentic or corrective RAG?](#q14)
15. (Medium) [How do you handle tables and PDFs in RAG?](#q15)
16. (Medium) [How do you reduce hallucination?](#q16)
17. (Hard) [How do you keep the index fresh?](#q17)
18. (Hard) [How do you enforce permissions in RAG?](#q18)
19. (Hard) [How do you choose k (number of chunks)?](#q19)
20. (Hard) [How do you make RAG fast and cheap?](#q20)

---

<a name="q1"></a>
## Q1. (Easy) Explain RAG end to end.
**Answer:** RAG means the LLM answers from documents we retrieve at query time, not only from what it memorised in training. It has two pipelines. An **offline indexing** pipeline turns documents into searchable chunks. An **online query** pipeline finds the best chunks for the question and passes them to the model with an instruction to answer only from them and cite sources.

**How it works:**

1. **Indexing (offline, once per document change)**
   - **Load:** PDF, HTML or DB rows become `Document(page_content, metadata)`.
   - **Split:** documents become chunks of a few hundred tokens, with overlap.
   - **Embed:** each chunk becomes a vector, for example 384 dims for bge-small or 768 for nomic-embed-text.
   - **Store:** vectors plus metadata (company, year, page, ACL) go into Qdrant or pgvector. Build a BM25 index too if you want hybrid search.
2. **Retrieval (online, per question)**
   - Embed the question with **the same embedding model**.
   - Run ANN search for the top-k chunks, with optional metadata filters (company = 3M, year = 2022).
   - Optionally fuse with BM25 and rerank with a cross-encoder.
3. **Generation**
   - The prompt holds a system instruction, the numbered context chunks and the question.
   - The LLM answers with citations like `[2]`, and the app maps `[2]` back to file and page.

```text
          OFFLINE                                   ONLINE
PDF → load → split → embed → vector DB     question → embed → top-k search → (rerank)
                                   ▲                                │
                                   └────────── same embedding model ┘
                                                     ↓
                             prompt = instructions + chunks + question → LLM → answer + [citations]
```

**Code (LangChain 1.x, local with Ollama):**
```python
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Indexing
docs = PyMuPDFLoader("3M_2022_10K.pdf").load()          # one Document per page, metadata["page"]
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)  # characters
chunks = splitter.split_documents(docs)
store = QdrantVectorStore.from_documents(
    chunks, OllamaEmbeddings(model="nomic-embed-text"),
    location=":memory:", collection_name="filings",
)

# 2. Retrieval
retriever = store.as_retriever(search_kwargs={"k": 5})

def format_docs(docs):
    return "\n\n".join(
        f"[{i}] (page {d.metadata.get('page')}) {d.page_content}" for i, d in enumerate(docs, 1)
    )

# 3. Generation
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer only from the context. Cite chunks like [1]. "
               "If the answer is not in the context, say \"I don't know\"."),
    ("human", "Context:\n{context}\n\nQuestion: {question}"),
])
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | ChatOllama(model="llama3.1", temperature=0)
    | StrOutputParser()
)
print(chain.invoke("What was 3M's capital expenditure in FY2022?"))
```

**Simple version:** An open-book exam: find the right pages, then answer using only those pages.

**Follow-up:** "Where does RAG usually fail?" Most failures are retrieval failures: the right chunk never reached the prompt. That is why you evaluate retrieval separately ([Q11](#q11)).

**Gotcha:** Changing the embedding model means re-embedding the whole corpus. Query vectors and document vectors from different models are not comparable.

**Tie to your project (P2):** "FinSight does exactly this over SEC filings, running locally on Ollama."

*Source ID: 6.1*

---

<a name="q2"></a>
## Q2. (Easy) Why RAG instead of fine-tuning?
**Answer:** RAG is the right tool for **knowledge**: facts that change often, that must be cited, or that need per-user access control, and it needs no training. Fine-tuning is the right tool for **behaviour**: output format, tone, domain style, or a narrow task done cheaply by a small model. It is poor at adding fresh facts, it can't cite, and every update means retraining. Many systems use both: fine-tune for format, RAG for facts.

| | RAG | Fine-tuning (e.g. LoRA) |
|---|---|---|
| Adds new or changing facts | Yes, re-index in minutes | Poorly, needs retraining and still hallucinates |
| Citations / traceability | Yes, chunk → page | No |
| Access control per user | Yes, filter at retrieval | No, the knowledge is baked into the weights |
| Changes style / format / skill | Weakly, via the prompt | Yes |
| Cost profile | Per query (longer prompts) | Up front (training) plus hosting |
| Data needed | Just the documents | Hundreds to thousands of labelled examples |

**Decision rule:** "If the problem is *the model doesn't know X*, use RAG. If it is *the model doesn't behave like Y*, fine-tune. If it is both, use both."

**Example:** A bank assistant answering from this quarter's policy PDFs should use RAG, because policies change and auditors want a source. A model that must always output a strict JSON schema for a classifier is a fine-tuning (or structured-output) problem.

**Simple version:** RAG gives the model a library card; fine-tuning sends it to a training course.

**Follow-up:** "Why not just use a 1M-token context window?" Cost and latency scale with tokens on every call, accuracy drops for facts in the middle of long contexts ("lost in the middle"), and you still need access control. Long context complements RAG; it doesn't replace it. See [System Design Q11](./14_System_Design.md#q11).

*Source ID: 6.2*

---

<a name="q3"></a>
## Q3. (Easy) How do you choose a chunking strategy and chunk size?
**Answer:** A chunk must be **small enough to be specific** (one idea, so its embedding isn't diluted) and **large enough to be self-contained** (the answer plus its context). I start with recursive splitting at a few hundred tokens and 10–20% overlap, use structure-aware splitting when the documents have headings, pages or tables, attach metadata to every chunk, and then **choose using retrieval metrics on an eval set**, not intuition.

**Strategies:**

| Strategy | How it splits | Good for | Weakness |
|---|---|---|---|
| Fixed size | Every N tokens | Baseline, logs | Cuts sentences and tables |
| Recursive (`RecursiveCharacterTextSplitter`) | Tries `\n\n`, then `\n`, then `" "`, then characters, until it fits | General prose, the default | Ignores document structure |
| Structure-aware | Markdown/HTML headers, PDF pages, sections | Filings, manuals, docs | Sections can be very uneven |
| Semantic | Breaks where embedding similarity between sentences drops | Mixed-topic text | Slower, less predictable sizes |
| Page-level / parent-child | Small chunks for search, the page or section for the LLM | When gold labels are pages | More storage, see [Q13](#q13) |

**Formula: chunk count and storage**
```text
n_chunks ≈ ceil((L − O) / (C − O))        L = doc tokens, C = chunk size, O = overlap
storage  ≈ n_chunks × dim × 4 bytes        (float32 vectors, before index overhead)
```
**Example:** A 10-K of about 100,000 tokens with C = 500 and O = 50 gives `ceil(99,950 / 450) = 223` chunks. With 768-dim vectors that is `223 × 768 × 4 ≈ 0.7 MB` per filing. 10,000 filings is about 7 GB of raw vectors.

**Size trade-off:**
- **Too small** (around 100 tokens): precise but missing context ("it increased 12%", but what did?). You need a larger k.
- **Too big** (2,000+ tokens): the embedding averages many topics, so similarity is fuzzy, and you waste prompt tokens.

**Code: token-based recursive splitting plus a contextual header**
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

# chunk_size counts CHARACTERS by default; from_tiktoken_encoder makes it count tokens
splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=500, chunk_overlap=75)
chunks = splitter.split_documents(docs)
for c in chunks:
    c.metadata.update({"company": "3M", "fiscal_year": 2022, "doc_type": "10-K"})
    c.page_content = f"3M 10-K FY2022, page {c.metadata['page']}\n{c.page_content}"
```

**Gotcha:** `chunk_size=1000` in `RecursiveCharacterTextSplitter` means 1,000 **characters** (about 250 tokens in English), not tokens. Interviewers like this one.

**Tie to your project (P2):** "I compared 4 chunking strategies and two embedding models; the best setup found the right filing 99% of the time and the gold page in the top 10 for 61%." \[Fill: the four strategies and the winner.\]

*Source ID: 6.3*

---

<a name="q4"></a>
## Q4. (Easy) What is chunk overlap and why use it?
**Answer:** Overlap means consecutive chunks share some text at their boundary, so a sentence or fact cut by a split still appears whole in at least one chunk. 10–20% of the chunk size is typical. Too much overlap stores near-duplicate chunks, inflates the index, and returns the same text twice in the top-k, which wastes context.

**Example (chunk size 10 words, overlap 3):**
```text
Text:    "Revenue grew 12% in FY2022 driven by healthcare. Margins fell due to ..."
Chunk 1: Revenue grew 12% in FY2022 driven by healthcare. Margins
Chunk 2:                        by healthcare. Margins fell due to ...
                                └── overlap ─┘
```
Without overlap, a question about "why margins fell" might match a chunk starting mid-thought with no subject.

**Formula: storage cost of overlap**
```text
step = C − O
extra chunks ≈ C / (C − O)    →   C=500, O=100: 500/400 = 1.25 → about 25% more chunks than no overlap
```

**Follow-up:** "Is overlap needed with structure-aware chunking?" Less so. If you split on section or paragraph boundaries, sentences aren't cut, so overlap can be small or zero.

**Gotcha:** With high overlap, deduplicate retrieved chunks (or use MMR, maximal marginal relevance: `search_type="mmr"`) so the top-5 isn't five copies of the same paragraph.

*Source ID: 6.4*

---

<a name="q5"></a>
## Q5. (Easy) How do vector databases search? What is ANN and HNSW?
**Answer:** A vector DB stores one embedding per chunk and, for a query vector, returns the k most similar vectors by cosine similarity, dot product or Euclidean distance. Exact search compares the query with every vector, which is O(N·d) and too slow at millions of vectors. So vector DBs use **approximate nearest neighbour (ANN)** indexes that trade a little recall for a large speed-up. **HNSW** is the most common one: a layered graph you search greedily from the top layer down, roughly O(log N).

**Similarity formulas:**
```text
cosine(q, d)  = (q · d) / (‖q‖ ‖d‖)          direction only; range −1..1
dot(q, d)     = Σ q_i d_i                     = cosine when both vectors are normalised to length 1
L2(q, d)      = sqrt(Σ (q_i − d_i)²)          smaller = closer
```
**Example:** q = [0.6, 0.8], d = [0.8, 0.6]. Both have length 1, so cosine = 0.6×0.8 + 0.8×0.6 = **0.96**, very similar.

**How HNSW works (Hierarchical Navigable Small World):**
- Every vector is a node linked to about **M** close neighbours.
- Upper layers are sparse (few nodes, long jumps); layer 0 has every node.
- Search starts at the top entry point, greedily moves to the closest neighbour, drops down a layer, and repeats. On layer 0 it keeps a candidate list of size **ef** and returns the best k.

```text
Layer 2:  A ─────────────── F                  (few nodes, highway)
Layer 1:  A ──── C ──── F ──── H
Layer 0:  A─B─C─D─E─F─G─H─I─J  (all nodes)     (local streets)
```

**Tuning knobs (same idea across DBs):**

| Knob | Qdrant / pgvector name | Effect |
|---|---|---|
| M | `m` | More links: better recall, more memory, slower build. 16 is typical |
| ef_construction | `ef_construct` / `ef_construction` | Build-time quality. 100–200 |
| ef (search) | `hnsw_ef` / `hnsw.ef_search` | Higher: better recall, slower query. Must be ≥ k |

**Other ANN families:** IVF (cluster into `lists`, search a few `probes`) and PQ / scalar quantisation (compress vectors 4–32×, lower memory, small recall loss).

**Simple version:** A smart map that jumps to the right neighbourhood instead of checking every house.

**Follow-up:** "How do you know ANN isn't hurting you?" Measure ANN recall against exact search on a sample of queries. Aim for at least 0.95, and raise `ef` if it is lower.

**Gotcha:** Use the distance metric the embedding model was trained for, usually cosine, and normalise vectors if you use dot product.

*Source ID: 6.5*

---

<a name="q6"></a>
## Q6. (Easy) How do you choose a vector store?
**Answer:** Start from what you already run and from your scale. **pgvector** when you already have Postgres and up to a few million vectors: one less system, transactions, SQL joins and filters with your own tables. A **dedicated vector DB** (Qdrant, Weaviate, Milvus, Pinecone) for larger scale, native hybrid search, fast filtered search, quantisation and horizontal scaling. **Chroma or FAISS** for prototypes and notebooks.

| Need | Pick |
|---|---|
| Already on Postgres, moderate scale, join with app data | pgvector (HNSW index) |
| Native hybrid (dense + sparse), rich payload filters, self-hosted | Qdrant / Weaviate |
| Billions of vectors, distributed | Milvus |
| Fully managed, no ops | Pinecone, or managed Qdrant/Weaviate |
| Local prototype | Chroma, FAISS (a library, not a DB) |

**Questions to ask before choosing:** How many vectors now and in a year? Are metadata filters needed (tenant, ACL, year)? Hybrid search? Latency target (p95)? Who operates it? Is managed cloud allowed for the data?

**Memory sizing example:** 5M chunks × 768 dims × 4 bytes ≈ **15.4 GB** of raw vectors, plus HNSW links. That decides whether you need quantisation or a bigger node.

**Code: switching store is a one-line change in LangChain**
```python
from langchain_postgres import PGVector

store = PGVector(
    embeddings=emb,
    collection_name="filings",
    connection="postgresql+psycopg://user:pass@localhost:5432/app",
)
```

**Gotcha:** Filtered search on a pure ANN index can lose recall when the filter is very selective. Qdrant handles this with payload indexes. In pgvector, check recall with filters too, not just without.

**Tie to your project (P2 and P4):** "FinSight uses Qdrant. For PNI Hub, which already runs Postgres, I'd consider pgvector first to avoid new infrastructure."

*Source ID: 6.6*

---

<a name="q7"></a>
## Q7. (Medium) What is hybrid search?
**Answer:** Hybrid search runs **dense (semantic) search and sparse (keyword, BM25) search together** and fuses the two ranked lists. Dense search understands meaning ("capital spending" ≈ "capex") but is weak on exact tokens such as tickers, years, product codes and names. BM25 nails exact tokens but misses paraphrases. Fusing them with Reciprocal Rank Fusion ([Q8](#q8)) or weighted scores usually beats either alone, especially on domain-heavy text.

**BM25 formula (the sparse side):**
```text
score(D, Q) = Σ_{t in Q} IDF(t) · f(t,D)·(k1 + 1) / ( f(t,D) + k1·(1 − b + b·|D|/avgdl) )
IDF(t)      = ln( (N − n_t + 0.5) / (n_t + 0.5) + 1 )

f(t,D) = count of term t in D,  |D| = doc length,  avgdl = average doc length
N = number of docs,  n_t = docs containing t,  k1 ≈ 1.2–2.0 (term saturation),  b ≈ 0.75 (length normalisation)
```
**In plain words:** rare terms count more (IDF), repeating a term helps but with diminishing returns (k1), and long documents are penalised so they don't win just by being long (b).

**Example:**

| Query | Dense finds | BM25 finds |
|---|---|---|
| "How much did 3M spend on capex in FY2022?" | Pages about "purchases of property, plant and equipment" ✓ | Pages containing "3M" and "FY2022" ✓ |
| "MMM 2022 PP&E purchases" | May drift to generic capex text ✗ | Exact "MMM", "PP&E" ✓ |

**Weighted fusion alternative:**
```text
score = α · norm(dense) + (1 − α) · norm(bm25)      norm = min-max per query, α ≈ 0.5–0.7
```
Weighted fusion needs score normalisation; RRF doesn't.

**Code, option A: Qdrant native hybrid (dense + BM25 sparse vectors)**
```python
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode

store = QdrantVectorStore.from_documents(
    chunks,
    embedding=emb,
    sparse_embedding=FastEmbedSparse(model_name="Qdrant/bm25"),
    retrieval_mode=RetrievalMode.HYBRID,
    location=":memory:",
    collection_name="filings_hybrid",
)
hybrid = store.as_retriever(search_kwargs={"k": 10})
```

**Code, option B: any two retrievers with `EnsembleRetriever` (weighted RRF)**
```python
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever   # needs: pip install rank_bm25

bm25 = BM25Retriever.from_documents(chunks, k=10)
dense = store.as_retriever(search_kwargs={"k": 10})
hybrid = EnsembleRetriever(retrievers=[bm25, dense], weights=[0.4, 0.6])
```

**Follow-up:** "What are learned sparse models?" SPLADE-style models learn which terms (and related terms) to weight. They sit between BM25 and dense.

**Tie to your project (P2):** "Filings are full of exact terms like '3M' and 'FY2022', so BM25 adds real value." \[Fill: lift over dense-only.\]

*Source ID: 6.7*

---

<a name="q8"></a>
## Q8. (Medium) What is Reciprocal Rank Fusion?
**Answer:** RRF merges several ranked lists using **only the rank positions, not the raw scores**. Each document gets `1 / (k + rank)` from every list it appears in, and these are summed. Documents ranked high in several lists win. Because BM25 scores (0 to 30+) and cosine scores (0 to 1) are on different scales, rank-based fusion avoids normalisation entirely, which is why it is the default for hybrid search.

**Formula:**
```text
RRF(d) = Σ_{r ∈ result lists} 1 / (k + rank_r(d))          k = 60 (from the original paper), rank starts at 1
Weighted RRF (LangChain EnsembleRetriever): Σ w_r / (k + rank_r(d))
```
**Why k = 60:** It flattens the curve so rank 1 doesn't dominate. 1/61 = 0.0164 versus 1/62 = 0.0161, a small gap, so agreement between lists matters more than a single top position.

**Worked example:**

| Doc | BM25 rank | Dense rank | RRF score | Final |
|---|---|---|---|---|
| A | 1 | 4 | 1/61 + 1/64 = 0.01639 + 0.01563 = **0.03202** | 2nd |
| B | 3 | 1 | 1/63 + 1/61 = 0.01587 + 0.01639 = **0.03226** | **1st** |
| C | 2 | — | 1/62 = **0.01613** | 3rd |
| D | — | 2 | 1/62 = **0.01613** | 3rd (tie) |

B wins even though it isn't first in BM25, because both retrievers like it.

**Code (from scratch, 6 lines, a good thing to write on a whiteboard):**
```python
from collections import defaultdict

def rrf(*ranked_lists, k=60):
    scores = defaultdict(float)
    for ranking in ranked_lists:
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] += 1 / (k + rank)
    return sorted(scores, key=scores.get, reverse=True)

print(rrf(["A", "C", "B"], ["B", "D", "E", "A"]))   # ['B', 'A', 'C', 'D', 'E']
```

**Gotcha:** RRF throws away how confident each retriever was. If one retriever is clearly better, use weights (or weighted score fusion) tuned on your eval set.

*Source ID: 6.8*

---

<a name="q9"></a>
## Q9. (Medium) What is reranking?
**Answer:** Reranking is a **two-stage retrieval**. Stage 1 cheaply fetches a wide candidate set (for example top 30–50 from hybrid search) for **recall**. Stage 2 uses a slower, more accurate model, usually a **cross-encoder** (Cohere Rerank, bge-reranker, FlashRank), that reads the question and each chunk *together*, scores relevance, and keeps the best 3–8 for **precision**. Because it costs one model call per candidate, you only rerank the top candidates, never the whole corpus.

**Pipeline:**
```text
question ──► hybrid search (top 30, about 20 ms) ──► cross-encoder scores 30 pairs (about 100–300 ms) ──► top 5 ──► LLM
                 recall stage                              precision stage
```

**Example:** For "3M FY2022 capex", the dense top-30 puts the cash-flow page at **rank 14** (surrounded by pages that mention "capital" in general). The reranker reads "Purchases of property, plant and equipment (PP&E) … 2022 … $1,749" with the question and moves it to **rank 1**. Without reranking, k = 5 would miss it.

**Code (LangChain 1.x, local cross-encoder):**
```python
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

reranker = CrossEncoderReranker(
    model=HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base"), top_n=5
)
retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=store.as_retriever(search_kwargs={"k": 30}),
)
docs = retriever.invoke("What was 3M's capex in FY2022?")
```
Hosted option: `from langchain_cohere import CohereRerank`. Lightweight CPU option: `FlashrankRerank` from `langchain_community.document_compressors`.

**Measure it:** Compare MRR and recall@5 with and without the reranker ([Q11](#q11)). Reranking should raise MRR. It can't raise recall@30, because it only reorders what stage 1 found.

**Gotcha:** A reranker can't fix a recall problem. If the right chunk isn't in the top 30, improve stage 1 first (hybrid search, filters, chunking).

**Tie to your project (P2):** "Reranking is one of FinSight's retrieval modes; it helps when the right page is retrieved but ranked low."

*Source ID: 6.9*

---

<a name="q10"></a>
## Q10. (Medium) Bi-encoder versus cross-encoder?
**Answer:** A **bi-encoder** encodes the query and each document **separately** into vectors and compares them with cosine similarity. Document vectors can be pre-computed and indexed, so search over millions takes milliseconds. That's what embedding models do. A **cross-encoder** feeds the query and document **together** into one transformer and outputs a relevance score. It sees word-level interactions, so it is more accurate, but it can't pre-compute anything and needs one forward pass per pair. So bi-encoders retrieve and cross-encoders rerank.

| | Bi-encoder | Cross-encoder |
|---|---|---|
| Input | `enc(q)`, `enc(d)` separately | `enc([q ; d])` jointly |
| Output | Two vectors → cosine | One relevance score |
| Pre-compute docs | Yes | No |
| Cost per query over N docs | 1 encode + ANN search | N model passes |
| Accuracy | Good | Better |
| Role | Stage 1 retrieval | Stage 2 reranking |
| Examples | bge-small, nomic-embed-text, OpenAI embeddings | bge-reranker, Cohere Rerank, ms-marco MiniLM |

**Cost example:** 1M chunks at about 5 ms per cross-encoder pass is about 83 minutes per query, which is impossible. 30 candidates is about 150 ms. That arithmetic is the whole reason for two-stage retrieval.

**Code:**
```python
from sentence_transformers import CrossEncoder, SentenceTransformer

docs = ["Purchases of PP&E were $1,749M in 2022.", "3M was founded in 1902."]
query = "3M capex 2022"

bi = SentenceTransformer("BAAI/bge-small-en-v1.5")
doc_vecs = bi.encode(docs, normalize_embeddings=True)       # pre-computable, stored in the vector DB
q_vec = bi.encode(query, normalize_embeddings=True)
print(doc_vecs @ q_vec)                                       # cosine scores

ce = CrossEncoder("BAAI/bge-reranker-base")
print(ce.predict([(query, d) for d in docs]))                 # joint scores, one pass per pair
```

**Follow-up:** "What is ColBERT?" Late interaction: it stores one vector per token and scores with MaxSim. It is more accurate than a bi-encoder and cheaper than a cross-encoder, but needs much more storage.

*Source ID: 6.10*

---

<a name="q11"></a>
## Q11. (Medium) How do you evaluate a RAG system?
**Answer:** I evaluate **retrieval and generation separately**, because they fail for different reasons. **Retrieval:** did the right chunk or page come back, and how high? Measure hit rate / recall@k, MRR, precision@k and nDCG against a labelled set of question → gold document/page. **Generation:** given the context, is the answer **faithful** (every claim supported), **correct** (matches the reference), **relevant**, and are the **citations** right? I use LLM-as-judge plus a human-reviewed sample. Every run is tied to a config (chunking, embedding model, k, reranker) so I can compare changes, and the eval runs in CI.

**Retrieval formulas:**
```text
Hit rate@k   = fraction of questions with ≥ 1 relevant item in the top k
Recall@k     = (relevant items in top k) / (total relevant items)        per question, then averaged
Precision@k  = (relevant items in top k) / k
MRR          = (1/|Q|) · Σ_q 1 / rank_q          rank_q = position of the first relevant item (0 if none found)
nDCG@k       = DCG@k / IDCG@k,  DCG@k = Σ_{i=1..k} rel_i / log2(i + 1)    rewards relevant items near the top
```

**Worked example (3 questions, gold page ranks = 1, 4, not found):**
```text
Hit rate@5 = 2/3 = 0.67
MRR        = (1/1 + 1/4 + 0) / 3 = 1.25 / 3 = 0.42
```
Hit rate says *did we find it*; MRR says *how high*. A reranker should raise MRR at the same hit rate.

**Generation metrics (RAGAS-style):**

| Metric | Question it answers | How it is computed |
|---|---|---|
| Faithfulness | Is every claim supported by the context? | Supported claims / total claims (LLM extracts and checks claims) |
| Answer correctness | Does it match the reference answer? | Semantic and factual overlap with the gold answer |
| Answer relevance | Does it address the question? | Similarity of questions regenerated from the answer to the original question |
| Context precision | Are the relevant chunks ranked high? | Rank-weighted precision of the retrieved context |
| Context recall | Does the context contain everything needed? | Reference claims covered by the context / total |
| Citation accuracy | Do the cited chunks actually say this? | Check each cited id against the claim |

**Code: retrieval metrics you can put in pytest**
```python
def hit_rate_and_mrr(results, gold, k=10):
    """results: {qid: [page ids ranked]}, gold: {qid: set of gold page ids}"""
    hits, rr = 0, 0.0
    for qid, ranked in results.items():
        for rank, page in enumerate(ranked[:k], start=1):
            if page in gold[qid]:
                hits += 1
                rr += 1 / rank
                break
    n = len(results)
    return hits / n, rr / n

def test_retrieval_does_not_regress():
    results = {"q1": ["p7", "p3"], "q2": ["p1", "p9", "p4"]}
    gold = {"q1": {"p7"}, "q2": {"p4"}}
    hit, mrr = hit_rate_and_mrr(results, gold)
    assert hit == 1.0 and round(mrr, 2) == 0.67
```

**Process:** Build a golden set (start with 50–200 real questions), run offline evals on every change, track the results in LangSmith experiments, sample production traces for human review, and add each failure back into the golden set. See [RAGAS and evaluation tools](./12_LangSmith_and_Evaluation.md#q15).

**Gotcha:** LLM-as-judge has bias (it favours long answers and its own model family). Calibrate it against human labels on a sample before trusting it.

**Tie to your project (P2):** "My 99% and 61% numbers are retrieval metrics on FinanceBench; runs are config-fingerprinted and covered by pytest."

*Source ID: 6.11*

---

<a name="q12"></a>
## Q12. (Medium) Why is your top-10 page retrieval only 61%?
**Answer:** "Filing-level retrieval is effectively solved at 99%. The 61% is the much stricter **page-level** hit rate@10: the exact gold page from FinanceBench must be in the top 10 out of a few hundred pages in a 10-K. The misses come from four causes, and each has a concrete fix."

| Cause | Why it hurts | Fix |
|---|---|---|
| **Boilerplate repeats** across pages and years | Many near-identical chunks compete, and the gold one gets pushed down | Metadata filters (company, fiscal year, section); dedupe / MMR |
| **Numbers live in tables** that chunk badly | Rows get split from their headers, so the embedding has no meaning | Table-aware parsing; keep tables whole with caption and headers ([Q15](#q15)) |
| **Vocabulary mismatch** ("capex" vs "purchases of PP&E") | Dense search misses domain synonyms, BM25 misses paraphrases | Hybrid search, query rewriting / multi-query, HyDE |
| **Strict labels** (a neighbouring page with the same number counts as a miss) | The metric undercounts useful retrieval | Also report a "page ± 1" or "answer-bearing chunk" metric |

**How to read the number:** If the reranker raised MRR but not hit rate@10, the problem is recall in stage 1, so fix chunking and filters before the reranker. Breaking misses down by question type (numeric from a table versus narrative) shows which fix to do first.

**How to say it:** Confident, not defensive: "Filing-level is solved; page-level is where the hard problem is, and here's my plan." Then name the next two experiments and how you would measure them (hit rate@10 and MRR on the same split, same config fingerprint).

**Gotcha:** Don't claim improvements you haven't measured. Say "I expect table-aware chunking to help most, because \[Fill: share of misses that are table questions\] of the misses are table questions."

*Source ID: 6.12*

---

<a name="q13"></a>
## Q13. (Medium) What advanced retrieval techniques do you know?
**Answer:** I group them by which problem they fix. **Query side:** multi-query, HyDE, query rewriting and decomposition. **Index side:** parent-document / small-to-big, contextual chunk headers, multi-vector summaries. **Filtering:** self-query / metadata filters. **Post-retrieval:** reranking, contextual compression, MMR. **Control flow:** agentic or corrective RAG in LangGraph. I pick based on the failure analysis, not because a technique is popular.

| Technique | Fixes | How it works | LangChain |
|---|---|---|---|
| Multi-query | Vocabulary mismatch | LLM writes 3–5 rephrasings; union of results | `MultiQueryRetriever` |
| HyDE | Short question vs long document | LLM writes a *hypothetical answer*; embed that instead of the question | Custom chain |
| Query decomposition | Multi-hop questions | "Compare 3M and GE capex" becomes two sub-queries | LangGraph / custom |
| Parent-document (small-to-big) | Precise search but too little context | Search small child chunks, return the larger parent section | `ParentDocumentRetriever` |
| Contextual chunk headers | Chunks lacking context | Prefix each chunk with doc, section and page titles before embedding | At split time ([Q3](#q3)) |
| Self-query / metadata filter | Wrong company or year retrieved | LLM extracts a filter (`company=3M, year=2022`) from the question | `SelfQueryRetriever` or structured output |
| Contextual compression | Long noisy chunks | Keep only relevant sentences or chunks | `ContextualCompressionRetriever` |
| MMR | Duplicate results | Balance relevance and diversity | `search_type="mmr"` |

**MMR formula:**
```text
MMR = argmax_{d ∉ S} [ λ · sim(d, q) − (1 − λ) · max_{s ∈ S} sim(d, s) ]     λ ≈ 0.5–0.7
```

**Code: multi-query and parent-document**
```python
from langchain_classic.retrievers import MultiQueryRetriever, ParentDocumentRetriever
from langchain_core.stores import InMemoryStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

multi = MultiQueryRetriever.from_llm(retriever=store.as_retriever(), llm=llm)

parent = ParentDocumentRetriever(
    vectorstore=store,                     # holds the small child chunks
    docstore=InMemoryStore(),              # holds the full parents
    child_splitter=RecursiveCharacterTextSplitter(chunk_size=400),
    parent_splitter=RecursiveCharacterTextSplitter(chunk_size=2000),
)
parent.add_documents(docs)
```

**HyDE in one line of theory:** the question "What drove margin decline?" looks nothing like a filing paragraph, but a *fake answer* ("Operating margin declined due to higher raw material costs and ...") looks very much like one, so its embedding lands near the real paragraph.

**How to say it:** Pick two you'd apply and say why. Example: "For FinSight I'd add **metadata filters** for company and year, because boilerplate from other years competes, and **parent-document retrieval**, because labels are page-level: search small chunks, return the page."

*Source ID: 6.13*

---

<a name="q14"></a>
## Q14. (Medium) What is agentic or corrective RAG?
**Answer:** Classic RAG is a fixed pipeline: retrieve once, then generate. **Corrective RAG** (CRAG) adds checks and loops. After retrieving, it **grades** whether the documents are relevant. If they aren't, it **rewrites the query** or searches another source (web, a different index) and retries. After generating, it can check that the answer is **grounded** in the documents, and otherwise retry or say "I don't know". **Adaptive RAG** adds a router up front: simple questions skip retrieval, hard ones get multi-step retrieval. **Agentic RAG** gives an agent retrieval as a *tool* and lets it decide when and what to search. LangGraph fits because these are graphs with conditional edges and loops.

**Graph:**
```text
START → retrieve → grade_docs ──relevant──► generate → check_grounded ──yes──► END
            ▲           │                                     │
            │      not relevant                               no
            └─ rewrite_query ◄────────────────────────────────┘   (stop after max_attempts → "I don't know")
```

**Code (LangGraph, compact):**
```python
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

class RAGState(TypedDict):
    question: str
    docs: list
    answer: str
    attempts: int

def retrieve(state: RAGState):
    return {"docs": retriever.invoke(state["question"]), "attempts": state["attempts"] + 1}

def grade(state: RAGState):
    keep = [d for d in state["docs"] if grader.invoke({"q": state["question"], "doc": d.page_content}).relevant]
    return {"docs": keep}

def route_after_grade(state: RAGState):
    if state["docs"]:
        return "generate"
    return "rewrite" if state["attempts"] < 3 else "give_up"

def rewrite(state: RAGState):
    return {"question": rewriter.invoke(state["question"]).content}

def generate(state: RAGState):
    return {"answer": rag_chain.invoke({"question": state["question"], "docs": state["docs"]})}

def give_up(state: RAGState):
    return {"answer": "I don't know based on the available documents."}

g = StateGraph(RAGState)
for name, fn in [("retrieve", retrieve), ("grade", grade), ("rewrite", rewrite),
                 ("generate", generate), ("give_up", give_up)]:
    g.add_node(name, fn)
g.add_edge(START, "retrieve")
g.add_edge("retrieve", "grade")
g.add_conditional_edges("grade", route_after_grade, ["generate", "rewrite", "give_up"])
g.add_edge("rewrite", "retrieve")
g.add_edge("generate", END)
g.add_edge("give_up", END)
app = g.compile()
app.invoke({"question": "3M capex FY2022?", "docs": [], "answer": "", "attempts": 0})
```
`grader` is a small LLM with structured output (`relevant: bool`), via `llm.with_structured_output(Grade)`.

**Trade-off:** each loop adds an LLM call, so latency and cost go up by 1.5–3×. Cap attempts, use a small, fast model for grading, and log every branch in LangSmith.

**Follow-up:** "Agentic RAG vs corrective RAG?" Corrective is a **fixed graph you designed**; agentic lets the **LLM choose** tools and steps. Corrective is more predictable and easier to evaluate, so I'd start there.

**Tie to your project (P2):** "The next step for FinSight is a corrective loop that re-queries when retrieved pages don't mention the asked metric."

*Source ID: 6.14*

---

<a name="q15"></a>
## Q15. (Medium) How do you handle tables and PDFs in RAG?
**Answer:** PDFs are layout, not text, so naive extraction scrambles columns and splits tables from their headers. I use a **layout-aware parser** (Docling, Unstructured, PyMuPDF) to separate text, headings and tables. I keep each **table as one chunk in Markdown or HTML** with its caption, column headers and page number. For retrieval, I often embed a **short text summary of the table** and return the **raw table** to the LLM (multi-vector retrieval). Page numbers stay in metadata for citations.

**Why tables break:**
```text
Naive extraction:  "2022 2021 Purchases of PP&E (1,749) (1,603) Net cash used ..."   ← which number is which year?
As Markdown:
| Item                     | 2022    | 2021    |
|--------------------------|---------|---------|
| Purchases of PP&E ($M)   | (1,749) | (1,603) |
```

**Pipeline:**
1. **Parse** with a layout-aware tool. Use OCR only for scanned pages, since it is slower and noisier.
2. **Classify** each element: heading, paragraph, table, figure.
3. **Text** → structure-aware chunks with a section header prefix.
4. **Tables** → one chunk each (split by rows only if huge, repeating headers), plus an LLM summary: *"Cash-flow table: capex (purchases of PP&E) 2022 vs 2021"*.
5. **Index** the summaries and text; map each summary id → raw table in a docstore.
6. **Generate** with the raw table plus a "cite page" instruction.

**Code: multi-vector (summary for search, raw table for the LLM)**
```python
import uuid

from langchain_classic.retrievers.multi_vector import MultiVectorRetriever
from langchain_core.documents import Document
from langchain_core.stores import InMemoryStore

retriever = MultiVectorRetriever(vectorstore=store, docstore=InMemoryStore(), id_key="doc_id")
ids = [str(uuid.uuid4()) for _ in tables]
summaries = [
    Document(page_content=summary, metadata={"doc_id": i, "page": t.metadata["page"]})
    for i, t, summary in zip(ids, tables, table_summaries)
]
retriever.vectorstore.add_documents(summaries)       # search on the summaries
retriever.docstore.mset(list(zip(ids, tables)))       # return the raw tables
```

**Gotcha:** LLMs are bad at arithmetic over large tables. For calculations (growth %, ratios), extract the numbers and compute them in Python (a tool call), then let the LLM explain.

**Tie to your project (P2):** "SEC filings are table-heavy; PDF parsing was a real part of the pipeline."

*Source ID: 6.15*

---

<a name="q16"></a>
## Q16. (Medium) How do you reduce hallucination?
**Answer:** Defence in depth, in priority order. **1. Better retrieval:** most hallucinations happen when the right context is missing, so the model fills the gap. **2. Strict prompt:** "answer only from the context; if it isn't there, say you don't know". **3. Citations:** require chunk ids per claim and **verify them in code**. **4. Decoding:** temperature 0 and structured output. **5. Post-check:** a groundedness / faithfulness check before returning, with a retry or refusal. **6. UX:** show sources so users can verify. Then measure faithfulness on an eval set ([Q11](#q11)) so you know it improved.

**Prompt pattern:**
```text
System: You answer questions about SEC filings.
Rules:
1. Use ONLY the numbered context below. Do not use prior knowledge.
2. After every factual sentence, cite the chunk like [2].
3. If the context does not contain the answer, reply exactly: "I don't know based on the provided filings."
4. Quote numbers exactly as written, with units and fiscal year.
```

**Code: structured answer plus citation verification**
```python
from pydantic import BaseModel

class Answer(BaseModel):
    answer: str
    citations: list[int]          # chunk numbers used
    found_in_context: bool

structured_llm = llm.with_structured_output(Answer)

def answer_with_checks(question, docs):
    result = structured_llm.invoke(prompt.format(context=format_docs(docs), question=question))
    valid_ids = set(range(1, len(docs) + 1))
    if not result.found_in_context or not result.citations or not set(result.citations) <= valid_ids:
        return "I don't know based on the provided filings."
    return result
```

**Groundedness metric:** `faithfulness = supported claims / total claims`. If it is below a threshold (for example 0.8) on a judge check, regenerate once or refuse.

**Follow-up:** "Does temperature 0 stop hallucination?" No. It makes output deterministic, not true. A wrong answer at temperature 0 is consistently wrong. Grounding comes from context and checks.

*Source ID: 6.16*

---

<a name="q17"></a>
## Q17. (Hard) How do you keep the index fresh?
**Answer:** **Incremental ingestion**, not full rebuilds. Each source document has a stable id plus a **content hash** and `updated_at`. On each sync, **new** documents are chunked and embedded, **unchanged** ones (same hash) are skipped, **changed** ones have their old chunks deleted and new ones written, and **deleted** sources have their chunks removed. LangChain's **indexing API with a record manager** does exactly this bookkeeping. It runs as a scheduled job or is triggered by events (webhooks, CDC), and answers show "as of" dates from metadata.

**Code (LangChain indexing API):**
```python
from langchain_classic.indexes import SQLRecordManager
from langchain_core.indexing import index

record_manager = SQLRecordManager("qdrant/filings", db_url="sqlite:///record_manager.db")
record_manager.create_schema()

result = index(
    chunks,                       # each chunk has metadata["source"]
    record_manager,
    store,
    cleanup="incremental",        # delete stale chunks of sources that changed
    source_id_key="source",
)
print(result)   # {'num_added': 12, 'num_updated': 0, 'num_skipped': 211, 'num_deleted': 9}
```

**Cleanup modes:**

| Mode | Deletes | Use when |
|---|---|---|
| `None` | Nothing, only dedupes | Append-only data |
| `"incremental"` | Old chunks of sources present in this batch | Continuous partial syncs |
| `"full"` | Everything not in this batch | The batch is the complete corpus |
| `"scoped_full"` | Like full, but only for sources seen in this batch | Large corpus synced in parts |

**Cost formula:** `re-embed cost per sync = changed_chunks × embed_cost`. Hashing means a nightly sync of 10,000 docs with 1% changes embeds about 100 docs, not 10,000.

**Other freshness concerns:**
- **Embedding model upgrade:** build a new collection in parallel (blue/green), run evals, switch the alias, and keep the old one for rollback.
- **Cache invalidation:** clear answer caches for affected sources.
- **Monitoring:** track index lag (`now − last_successful_sync`) and alert on it.

**Gotcha:** Chunk ids must be deterministic (hash of source + content). Random ids on every run duplicate the whole index.

**Tie to your project (P4):** "PNI Hub already runs 10 scheduled jobs for sync and cache warming; index refresh would be one more."

*Source ID: 6.17*

---

<a name="q18"></a>
## Q18. (Hard) How do you enforce permissions in RAG?
**Answer:** **Filter at retrieval time, inside the vector query, never after generation.** Every chunk carries ACL metadata copied from its source (allowed groups, tenant id, classification). At query time the app resolves the user's groups from the identity provider and passes them as a **pre-filter**, so unauthorised chunks are never scored, never in the prompt, and can't leak through the answer or citations. ACLs are synced from the source system (AD groups, Confluence spaces, SharePoint) on the same schedule as content.

**Why not filter afterwards?** If a confidential chunk reaches the prompt, the LLM may paraphrase it. You can't reliably "un-say" it. Post-filtering also breaks k: you ask for 10 and are left with 2.

**Code (Qdrant pre-filter through LangChain):**
```python
from qdrant_client import models

def retriever_for(user_groups: list[str], tenant_id: str):
    acl_filter = models.Filter(must=[
        models.FieldCondition(key="metadata.tenant_id", match=models.MatchValue(value=tenant_id)),
        models.FieldCondition(key="metadata.allowed_groups", match=models.MatchAny(any=user_groups)),
    ])
    return store.as_retriever(search_kwargs={"k": 10, "filter": acl_filter})

docs = retriever_for(["finance-analysts", "all-staff"], tenant_id="acme").invoke("Q3 budget")
```
pgvector equivalent: `search_kwargs={"filter": {"allowed_groups": {"$in": user_groups}}}`. With SQL you can also enforce Postgres row-level security.

**Checklist:**
- Groups come from the **server-side token** (Azure AD claims), never from the request body.
- Index the ACL fields (Qdrant payload index) so filtered search stays fast and accurate.
- Apply the same filter to BM25, caches and the "related documents" UI. Cache keys must include the user's permission scope.
- Revocation: ACL changes must propagate fast. Re-sync metadata only; no re-embedding needed.
- Test it: an automated test where user A must never retrieve user B's documents.

**Gotcha:** A shared answer cache keyed only on the question text leaks answers across users. Key it on `(question, permission_scope)`.

**Tie to your project (P4):** "Azure AD groups from PNI Hub would drive the retrieval filter."

*Source ID: 6.18*

---

<a name="q19"></a>
## Q19. (Hard) How do you choose k (number of chunks)?
**Answer:** There are two k's. **Retrieve wide** (k = 20–50) to maximise recall, **rerank**, then **send few** (k = 3–8) to the LLM for precision, cost and latency. I choose both values empirically: plot recall@k against k on the eval set and pick the knee of the curve for retrieval, then sweep the final k against answer faithfulness and correctness, within a token budget.

**Formulas:**
```text
Token budget:   system + question + k × chunk_tokens + answer_tokens ≤ context_limit
                with a cost target: k_max = (budget − system − question − answer) / chunk_tokens
Example:        budget 4,000 tokens, system 300, question 50, answer 500, chunks 500
                k_max = (4,000 − 850) / 500 = 6.3  →  k = 6
Cost per query: (prompt_tokens × input_price) + (answer_tokens × output_price)
```

**Example of a recall curve (illustrative):**

| k | 1 | 3 | 5 | 10 | 20 | 50 |
|---|---|---|---|---|---|---|
| Hit rate@k | 0.30 | 0.45 | 0.52 | 0.61 | 0.70 | 0.78 |

Reading it: going from 10 to 20 still adds 9 points, so retrieve 20–30 and rerank down to 5. Going from 20 to 50 adds less per extra chunk, and the reranker cost grows linearly.

**Why "more chunks" isn't always better:**
- **Lost in the middle:** models use information at the start and end of a long context better than in the middle, so extra chunks can bury the right one.
- More distractors give more chances to cite the wrong number.
- Cost and latency grow linearly with prompt tokens.

**Follow-up:** "Dynamic k?" Yes: use a reranker score threshold (keep chunks scoring above x, with a cap of 8), so easy questions send 2 chunks and hard ones send 8.

**Gotcha:** Put the highest-ranked chunks first (or first and last) in the prompt, not in random order.

*Source ID: 6.19*

---

<a name="q20"></a>
## Q20. (Hard) How do you make RAG fast and cheap?
**Answer:** First measure where time and money go (trace with LangSmith). In most systems **LLM generation dominates**, then the reranker, then retrieval. Then: **send fewer tokens** (smaller final k, compressed chunks), **use smaller models** where quality allows (a small model for grading and routing, a big one only for the answer), **cache** at every layer (embeddings, retrieval results, final answers, prompt prefixes), **use ANN plus quantisation** for search, **rerank only the top candidates**, **run retrieval branches in parallel**, and **stream** so the perceived latency is time to first token.

**Typical latency budget (illustrative, per query):**

| Step | Time | Lever |
|---|---|---|
| Embed question | 10–30 ms | Small local model (bge-small), cache |
| Hybrid ANN search | 10–50 ms | HNSW `ef`, quantisation, payload indexes |
| Rerank 30 candidates | 100–300 ms | Smaller reranker, fewer candidates, GPU |
| LLM generation | 1–5 s | Fewer prompt tokens, smaller model, streaming |

**Cost formula:**
```text
cost/query = embed_cost + (prompt_tokens × input_price + output_tokens × output_price)
prompt_tokens ≈ system + question + k × chunk_tokens
Cutting k from 10 to 5 at 500 tokens/chunk saves 2,500 input tokens per query, often about half the cost.
```

**Code: caching and parallel retrieval**
```python
from langchain_classic.embeddings import CacheBackedEmbeddings
from langchain_classic.storage import LocalFileStore
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
from langchain_core.runnables import RunnableParallel

# 1. Embedding cache: never embed the same chunk twice
cached_emb = CacheBackedEmbeddings.from_bytes_store(
    emb, LocalFileStore("./emb_cache"), namespace="nomic-embed-text"
)

# 2. Exact-match LLM cache (use Redis or a semantic cache in production)
set_llm_cache(InMemoryCache())

# 3. Run dense and BM25 in parallel instead of one after the other
both = RunnableParallel(dense=dense_retriever, sparse=bm25_retriever)
results = both.invoke("3M capex FY2022")
```
Async: `await chain.ainvoke(...)` / `astream(...)` inside Django or FastAPI views so requests don't block workers. See [Streaming and async](./11_Streaming_and_Async.md).

**More levers:**
- **Semantic cache:** if a new question's embedding is very close to a cached question (cosine > 0.95) *and* has the same permission scope, return the cached answer.
- **Provider prompt caching:** keep the static system prompt first so the provider caches the prefix.
- **Routing:** skip retrieval for chit-chat, and send easy questions to a small model.
- **Quantisation:** int8 or binary vectors cut memory 4–32×; rescore the top candidates with full vectors.

**Gotcha:** Don't optimise blindly. A cheaper setup that drops faithfulness is a regression, so run the eval set ([Q11](#q11)) after every speed or cost change.

**Tie to your project (P2):** "bge-small runs locally and fast, which is why it was worth comparing against a hosted embedding model."

*Source ID: 6.20*
