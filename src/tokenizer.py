import string
def tokenize(text: str) -> list[str]:
    text = text.lower()

    cleaned = ""
    for char in text:
        if char not in string.punctuation:
            cleaned += char
    return cleaned.split()
    
    