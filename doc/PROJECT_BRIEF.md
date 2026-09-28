# Hybrid-Search: Project Brief

## Purpose

Build a search engine from scratch that combines **keyword search (BM25)** and **semantic search (embeddings)**, merges their rankings, serves it through an API, and proves it works with real benchmark numbers.

Goals:
1. Learn search/IR fundamentals well enough to explain and whiteboard them in interviews.
2. Ship a finished, tested, deployed project for a SWE/AI internship resume (2nd-year UofT CS, applying for Summer 2027).

Non-goal: competing with Meilisearch/Typesense. This is "built it, benchmarked it, here are the tradeoffs."

## The idea in plain language

A library of ~5,000 documents. Two helpers:
- **Word Finder (BM25):** an index of which documents contain which words, ranked by how well they match. Fast and precise, but only matches exact words ("car" will not find "automobile").
- **Meaning Finder (vectors):** turns text into numbers so similar meanings are close together. Handles paraphrases, but can miss exact terms and names.

**Hybrid:** run both, fuse the two ranked lists, and get the strengths of each.

## Architecture

```
Documents -> Tokenizer -> Inverted Index -> BM25 scores ----+
                                                             +-> RRF fusion -> Ranked results
Documents -> Embedding model -> Vector store -> Cosine sim --+

Queries go through the same tokenizer / embedding model as documents.
```

## Repo layout

```
Hybrid-Search/
  src/
    tokenizer.py     tokenize(text) -> list[str]
    index.py         InvertedIndex class
    (later) bm25.py, vector.py, fusion.py, api.py
  tests/             pytest tests, one file per module
  scripts/get_data.py  downloads BEIR SciFact into data/
  data/              dataset (gitignored)
  docs/PROJECT_BRIEF.md  this file: the whole project, stable
  docs/STATUS.md         current phase, next steps, decisions log, open questions
  LEARNING.md        my notes: what I learned, what confused me
  pytest.ini         testpaths = tests
```

`src/` is reusable library code and never imports from `scripts/`. `tests/` imports from `src/`.

## Stack

Python 3.11, numpy, pytest, `beir` (data loading), sentence-transformers (`all-MiniLM-L6-v2`, CPU), FastAPI + uvicorn, Docker, GitHub Actions, ranx or ir_measures (metrics). FAISS only as a later optimization. `rank_bm25` only to cross-check my own BM25.

## Phases

Current progress, next steps, and decisions live in `docs/STATUS.md`. This file stays stable.

| Phase | What |
|---|---|
| 0 | Setup, dataset download, Git + GitHub |
| 1 | Tokenizer + tests |
| 2 | Inverted index |
| 3 | BM25 ranking |
| 4 | Vector search (embeddings, brute-force cosine) |
| 5 | Fusion (reciprocal rank fusion) |
| 6 | Benchmarking on SciFact: recall@10, nDCG@10, p50/p99 latency for BM25 vs vector vs hybrid |
| 7 | FastAPI wrapper, Docker, GitHub Actions CI |
| 8 | Deploy (DigitalOcean/Azure via student credits), README with benchmarks and tradeoffs |

## Phase details

**Phase 1: Tokenizer (done).** Lowercase, delete punctuation, split on whitespace. Tests cover case, punctuation, extra whitespace, empty string.

**Phase 2: Inverted index.** `InvertedIndex` with:
- `postings`: word -> {doc_id: term_frequency}
- `doc_lengths`: doc_id -> token count
- `add_document(doc_id, text)`, `get_postings(word)`, `num_docs()`, `avg_doc_length()`, `search_and(query)`, `search_or(query)`
- Term frequency and doc lengths are stored now because BM25 needs them.
- Edge cases: unknown word returns `{}`, empty query returns empty set, repeated words increase the count.
- After tests pass: index all 5,183 SciFact docs and time it.

**Phase 3: BM25.** Score documents using term frequency, inverse document frequency, and document length normalization (parameters k1 and b). Implement myself in numpy, then cross-check a few scores against `rank_bm25`. Must be able to explain why IDF, why length normalization, and why it beats raw counts.

**Phase 4: Vector search.** Embed docs with `all-MiniLM-L6-v2` (384 dims). Brute-force cosine similarity via numpy matrix multiply first. Test on paraphrase queries BM25 misses.

**Phase 5: Fusion.** Reciprocal rank fusion, `score(d) = sum over lists of 1/(k + rank)`, k around 60. Explain why rank-based fusion instead of averaging raw scores (BM25 and cosine live on different scales).

**Phase 6: Benchmarking.** SciFact test split with qrels. Compare BM25-only, vector-only, and hybrid on recall@10, nDCG@10, and latency p50/p99. Report honestly, even if hybrid does not win.

**Phase 7: Productionize.** FastAPI (`POST /index`, `GET /search?q=...&mode=hybrid`), Dockerfile, GitHub Actions running pytest on every push.

**Phase 8: Deploy + document.** Live URL, README with architecture diagram, benchmark table, and at least one honest tradeoff.

## Rules for myself

- Write Phases 1-3 by hand. AI explains and reviews; it doesn't generate.
- Tests first, small and single-assert.
- After each phase: close every AI tool, explain it from memory, and write it in `LEARNING.md`.
- Commit after each meaningful chunk (`git add .`, `git commit -m "..."`, `git push`).
- Apply to internships in parallel, not after the project is done.

## Resume target (fill in real numbers only after Phase 6)

"Built a hybrid BM25 + vector search engine with reciprocal rank fusion; achieved X% higher recall@10 than BM25-only at p99 latency of Y ms on BEIR SciFact; CI-tested and deployed as a containerized FastAPI service."
