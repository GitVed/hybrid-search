# LEARNING.md

Notes on the concepts behind each phase of Hybrid-Search. Scope: project and phase learning only (search, ranking, embeddings, benchmarking, systems tradeoffs). 

_Last updated: 2026-09-27_

---

## Big picture (in my own words)

A search engine has to find the right documents out of thousands without reading every one on each query.

- **Keyword search (BM25)** looks up exact words in an index. Fast and precise, but "car" won't find "automobile".
- **Vector search** turns text into numbers so similar meanings sit close together. It handles paraphrases but can miss exact terms like names or error codes.
- **Hybrid** runs both and merges the two ranked lists, so each covers the other's weakness.
- **Benchmarking** (recall@10, nDCG@10, latency) is what turns "I built a thing" into "I proved it works".

Pipeline: documents -> tokenizer -> inverted index -> BM25, and documents -> embeddings -> cosine similarity, then fusion -> ranked results. Queries go through the same processing as documents.

---

## Phase 1: Tokenizer

**What it does:** turns raw text into a clean list of lowercase terms with punctuation removed. This is the first step for both documents and queries.

**Final logic:** lowercase -> delete punctuation -> split on whitespace.

### Design decisions and tradeoffs
- **Punctuation is deleted, not replaced with a space.** `"cell's"` becomes `"cells"`, one token, instead of `"cell"` + `"s"`. Tradeoff: possessives and contractions merge with other words. Revisit only if benchmark results suffer.
- **Clean the whole string, then split.** Splitting first would leave punctuation attached to each token and force me to clean every token separately.
- **The same tokenizer must process documents and queries.** If they differ, terms silently fail to match. Classic search bug.
- **Deferred on purpose:** stemming, stopword removal, unicode handling. Add after Phase 6 and re-benchmark to see if they measurably help.

---

## Phase 2: Inverted index

**Concept:** a map from each term to the documents containing it, like a textbook's back-of-book index. Instead of scanning every document per query, I look up the term and read its postings.

**Structure:**
- `postings: term -> {doc_id: term_frequency}`
- `doc_lengths: doc_id -> token count`

**Why store term frequency now?** BM25 (Phase 3) needs it. A set of doc IDs alone would force a rebuild later.

**Why store document lengths?** Long documents repeat words just because they're long. BM25's length normalization corrects for this.

**Why a dict?** Lookup by key is average O(1). Scanning a list is O(n). Over 5,183 documents that's one lookup versus thousands of comparisons.

### Questions to answer in my own words (fill in after building it)
- [ ] What's the time complexity of a lookup vs scanning every document?
- [ ] How does `search_and` combine the postings of multiple terms?
- [ ] How does memory grow with corpus size?
- [ ] How would the index handle a document being updated or deleted?
- [ ] What did indexing all 5,183 SciFact docs cost in time and memory?

---

## Phase 3: BM25 (fill in as I learn it)

- [ ] Why raw term counts are a bad ranking signal
- [ ] What IDF captures and why rare terms matter more
- [ ] Why term frequency saturates (the role of k1)
- [ ] What length normalization does (the role of b)
- [ ] Why BM25 usually beats plain TF-IDF
- [ ] How my scores compare to `rank_bm25` on the same query

## Phase 4: Vector search (fill in as I learn it)

- [ ] What an embedding is and what the 384 dimensions represent
- [ ] Why cosine similarity instead of Euclidean distance
- [ ] Why brute-force is fine at 5k docs and where it breaks
- [ ] Queries where vector search wins and where it fails

## Phase 5: Fusion (fill in as I learn it)

- [ ] Why BM25 and cosine scores can't be averaged directly
- [ ] How reciprocal rank fusion works and what k does
- [ ] Cases where hybrid loses to a single method

## Phase 6: Benchmarking (fill in as I learn it)

- [ ] What recall@10 and nDCG@10 each measure, and where they disagree
- [ ] Why latency is reported as p50/p99 and not just average
- [ ] My results table and one honest finding

## Phases 7-8: Serving and deploy (fill in as I learn it)

- [ ] One systems tradeoff I hit (index build time vs query speed, memory vs latency, batch size)
- [ ] What breaks as the corpus grows, and what I'd change

---

## Self-check before moving on

Close all AI tools and answer out loud:
1. What does the tokenizer do, in what order, and why?
2. Why must queries and documents use the same tokenizer?
3. What is an inverted index and why is it fast?
4. Why is term frequency stored in the index even though Phase 2 doesn't rank anything?
5. Keyword vs vector search: what does each miss, and how does hybrid fix it?

If I stumble on any of these, that's the section to redo.
