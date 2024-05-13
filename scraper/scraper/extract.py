import requests
import unicodedata
from itertools import groupby
from readability import Document
from scraper.utils import HTMLStripper, tokenize_sentences


class ScrapeWebsite:
    """

    Get Text Content from Any Given Website

    Usage:
        article = ScrapeWebsite(website_url)

    Returns:
        self.text_content contains the content of the webpage
        self.separated_sentences contains sentences of the webpage in a list

    """

    def __init__(self, website_url):
        self.text_content = ""
        self.req = requests.get(
            website_url, headers=self.get_rand_headers(), timeout=10
        )
        self.retrieve_important()
        self.sentences = tokenize_sentences(self.text_content)
        self.strip_long_spaces()
        self.remove_escape_chars()

    def get_rand_headers(self):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/56.0.2924.76 Safari/537.36",
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
        }

    def strip_tags(self, html_content):
        html_stripper = HTMLStripper()
        html_stripper.feed(html_content)
        return html_stripper.get_data()

    def retrieve_important(self):
        article_content = Document(self.req.text)
        html_text = article_content.summary()
        self.text_content = self.strip_tags(html_text)
        self.text_content = self.normalize_data(self.text_content)

    def normalize_data(self, data_content):
        return unicodedata.normalize("NFKD", data_content)

    def format_sentences(self):
        index_sentence = 0
        for individual_sentence in self.sentences:
            if "\n\n" in individual_sentence:
                self.sentences[index_sentence] = " ".join(
                    individual_sentence.rsplit("\n\n", 1)[1:]
                )
            index_sentence += 1

    def remove_escape_chars(self):
        self.format_sentences()
        self.sentences = [
            individual_sentence.replace("\n", "").strip()
            for individual_sentence in self.sentences
        ]

    def return_article(self):
        return " ".join(individual_sentence for individual_sentence in self.sentences)

    """
    
    Strips consecutive whitespace from input 
    (Source: https://stackoverflow.com/a/12505450)
    
    """

    def strip_long_spaces(self, max_specified=5):
        for individual_sentence in self.sentences:
            current_max = 0

            # First, break the string up into individual strings for each space
            split_string = individual_sentence.split(" ")

            # Iterate over the list returning each string
            for c, sub_group in groupby(split_string):
                if c != "":
                    continue

                # Get the length of the run of spaces
                i = len(list(sub_group))

                if i > current_max:
                    current_max = i

            if current_max > max_specified:
                self.sentences.remove(individual_sentence)
