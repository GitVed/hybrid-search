# Hybrid Search

A from-scratch information-retrieval project exploring how lexical search and semantic search can work together. The long-term goal is to build and evaluate a hybrid search engine on the BEIR SciFact benchmark.

> **Status:** Early development. The tokenizer and core inverted-index operations are implemented. BM25, vector search, rank fusion, benchmarking, and the API are planned, not implemented yet.

## What it does today

- Tokenizes text by lowercasing, deleting punctuation, and splitting on whitespace.
- Builds an inverted index mapping each term to document IDs and term frequencies.
- Tracks document lengths for later BM25 scoring.
- Supports document count, average document length, postings lookup, and AND search.
- Includes pytest coverage for the tokenizer and index.

## Project direction

The planned search pipeline is:

```text
Documents -> Tokenizer -> Inverted index -> BM25 ranking ----+
                                                               +-> Rank fusion -> Results
Documents -> Embeddings -> Vector search ---------------------+
```

The project will compare lexical, semantic, and hybrid retrieval using SciFact relevance judgments. Benchmark results will be added after the evaluation is implemented and run.

## Requirements

- Python 3.11
- `pytest` to run tests
- `beir` to download and load the SciFact dataset with the provided script

## Setup

Create and activate a virtual environment, then install the packages needed for the current tests:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install pytest
```

Run the test suite from the repository root:

```powershell
python -m pytest
```

To download SciFact data, install BEIR and run the download script:

```powershell
python -m pip install beir
python scripts/get_data.py
```

The dataset is downloaded under `data/`, which is excluded from Git. The script loads the test split and prints the number of documents and queries.

## Example

```python
from src.index import InvertedIndex

index = InvertedIndex()
index.add_document("doc-1", "Cats are small mammals")
index.add_document("doc-2", "Dogs are mammals")

print(index.get_postings("mammals"))
# {'doc-1': 1, 'doc-2': 1}

print(index.search_and("cats mammals"))
# {'doc-1'}

print(index.num_docs())
# 2
```

`search_and()` returns a set of matching document IDs. An empty or unmatched query returns an empty set. `get_postings()` returns a dictionary mapping matching document IDs to term frequencies; for an unknown term it returns an empty dictionary.

## Repository layout

```text
src/            Tokenizer and inverted-index implementation
 tests/         Pytest tests
scripts/        Dataset download and loading
 data/          Downloaded SciFact data (gitignored)
doc/            Project brief and development status
LEARNING.md     Notes on information-retrieval concepts
```

## Roadmap

- [x] Text tokenizer
- [ ] Complete inverted-index phase, including OR search and indexing/timing the SciFact corpus
- [ ] Implement and validate BM25 ranking
- [ ] Add embedding-based vector search
- [ ] Combine ranked results with reciprocal rank fusion
- [ ] Benchmark BM25, vector, and hybrid retrieval on SciFact
- [ ] Add an API, containerization, CI, and deployment

See [`doc/PROJECT_BRIEF.md`](doc/PROJECT_BRIEF.md) for the full project plan and [`doc/STATUS.md`](doc/STATUS.md) for current progress.
