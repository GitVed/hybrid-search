from src.index import InvertedIndex

def test_get_postings():
    index = InvertedIndex()
    index.add_document("d1", "the cat sat")
    index.add_document("d2", "the cat saw the dog")
    index.add_document("d3", "the dog ran")

    assert index.get_postings("cat") == {"d1": 1, "d2": 1}

def test_doc_lengths():
    index = InvertedIndex()
    index.add_document("d1", "the cat sat")
    index.add_document("d2", "the cat saw the dog")
    index.add_document("d3", "the dog ran")

    assert index.doc_lengths == {"d1": 3, "d2": 5, "d3": 3}

def test_num_docs():
    index = InvertedIndex()
    index.add_document("d1", "the cat sat")
    index.add_document("d2", "the cat saw the dog")
    index.add_document("d3", "the dog ran")

    assert index.num_docs() == 3

def test_get_posting_repeated_word():
    index = InvertedIndex()
    index.add_document("d1", "cat cat dog CAT")

    assert index.get_postings("cat") == {"d1": 3}

def test_avg_doc_length():
    index = InvertedIndex()
    index.add_document("d1", "the cat sat")
    index.add_document("d2", "the cat saw the dog")
    index.add_document("d3", "the dog ran")

    assert index.avg_doc_length() == (11/3)


def test_search_and_general():
    index = InvertedIndex()
    index.add_document("d1", "the cat sat")
    index.add_document("d2", "the cat saw the dog")
    index.add_document("d3", "the dog ran")

    assert index.search_and("cat dog") == {"d2"}

def test_search_and_no_intersection():
    index = InvertedIndex()
    index.add_document("d1", "the cat sat")
    index.add_document("d2", "the cat saw the dog")
    index.add_document("d3", "the dog ran")

    assert index.search_and("hippo dog cat") == set()

def test_search_and_empty_query():
    index = InvertedIndex()
    index.add_document("d1", "the cat sat")
    index.add_document("d2", "the cat saw the dog")
    index.add_document("d3", "the dog ran")

    assert index.search_and("") == set()

def test_search_and_all_unknown_words():
    index = InvertedIndex()
    index.add_document("d1", "the cat sat")
    index.add_document("d2", "the cat saw the dog")
    index.add_document("d3", "the dog ran")

    assert index.search_and("hippo lion bird") == set()
    
def test_search_and_empty_text():
    index = InvertedIndex()
    index.add_document("d1", "")
    index.add_document("d2", "")

    assert index.search_and("cat dog") == set()

def test_search_and_empty_index():
    index = InvertedIndex()

    assert index.search_and("dog cat") == set()

