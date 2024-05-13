import spacy


spacy_preprocessor = None


class SpacyPreprocessor:
    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_lg")


def get_spacy_preprocessor() -> SpacyPreprocessor:
    global spacy_preprocessor

    if spacy_preprocessor is None:
        spacy_preprocessor = SpacyPreprocessor()

    return spacy_preprocessor
