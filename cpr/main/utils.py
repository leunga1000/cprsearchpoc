import string
def transform_text(text: str) -> str:
    return text.translate(str.maketrans('', '', string.punctuation)).lower()

try:
    import spacy
    spacy_nlp = spacy.load("en_core_web_md")
except ImportError:
    spacy_nlp = None
