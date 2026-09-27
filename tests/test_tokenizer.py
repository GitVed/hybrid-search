from src.tokenizer import tokenize

def test_lowercases():
    assert tokenize("HELLO") == ["hello"]

def test_whitespaces():
    assert tokenize(" OneWS  TwoWS   ThreeWS    ") == ["onews", "twows", "threews"]

def test_punctuation():
    assert tokenize("This!has?Weird][{]Text@<=>") == ["thishasweirdtext"]

def test_all_cases():
    assert tokenize("This ! HAS []<> all     the CASES ** in ?one@") == ["this", "has", "all", "the", "cases", "in", "one"]

def test_empty_string():
    assert tokenize("") == []
