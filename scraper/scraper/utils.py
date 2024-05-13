from abc import ABC
from io import StringIO
from html.parser import HTMLParser
import nltk

nltk.download("punkt", quiet=True)


class HTMLStripper(HTMLParser, ABC):
    """

    Strip HTML tags from string
    (Source: https://stackoverflow.com/a/925630)

    Usage:
        html_stripper = HTMLStripper()
        html_stripper.feed(html_content)
        print(html_stripper.get_data())

    Returns:
        String without HTML tags

    """

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def tokenize_sentences(input_Text):
    tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
    return tokenizer.tokenize(input_Text)
