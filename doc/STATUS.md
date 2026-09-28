# Status

Update this at the end of every work session. The stable overview is in `PROJECT_BRIEF.md`.

_Last updated: 2026-09-27_

## Current phase

**Phase 2: Inverted index** (`src/index.py`, `tests/test_index.py`)

Done so far:
- Phase 0: repo structure, venv, SciFact download, Git + GitHub
- Phase 1: tokenizer with 5 passing tests

In progress:
- [ ] Write tests in `tests/test_index.py` first
- [ ] Implement `InvertedIndex`
- [ ] Index all 5,183 SciFact docs and time it
- [ ] Write design notes in `LEARNING.md`

## Next up

1. Finish Phase 2, then commit and push.
2. **Phase 3: BM25.** Score docs using TF, IDF, and length normalization. Cross-check a few scores against `rank_bm25`.
3. Phase 4: embeddings and brute-force cosine similarity.

## Decisions log

Format: date, decision, one-line reason. Put the longer "why" in `LEARNING.md`.

| Date | Decision | Reason |
|---|---|---|
| 2026-09 | Dataset is BEIR SciFact | Small (~5k docs), has built-in relevance judgments |
| 2026-09 | Tokenizer deletes punctuation instead of replacing with a space | Simple; contractions merge ("cell's" -> "cells") |
| 2026-09 | Tokenize order: lowercase, strip punctuation, then split | Splitting last avoids cleaning each token separately |
| 2026-09 | Index stores `word -> {doc_id: term_freq}`, not just a set of doc IDs | BM25 needs term frequency |
| 2026-09 | Index also stores `doc_lengths` | BM25 length normalization |
| 2026-09 | Phases 1-3 written by hand; AI explains and hints only | Interview readiness |
| 2026-09 | Use VS Code plus chat assistant, not an agentic IDE | Keeps me typing the core logic |

## Open questions

- Keep or strip apostrophes? Currently stripped. Revisit only if it hurts benchmark results.
- Stemming / stopwords: skipped for v1. Try after Phase 6 and re-benchmark.

## Blockers

None right now.
