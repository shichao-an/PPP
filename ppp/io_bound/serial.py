import json
import re
import requests
from ppp.utils import db
from ppp.utils.decorators import timing
from .data.settings import (WIKIPEDIA_API_URL, WIKIPEDIA_API_QUERY_PARAMS,
                            COMMON_WORDS)


def semantic_parse(text):
    raw_words = text.split()
    cleaned_words = clean_words(raw_words)
    candidates = []
    return candidates


def clean_words(words):
    """
    Clean words by removing apostrophes, commas, periods, quotation marks, etc.

    """
    cleaned_words = []
    for word in words:
        s = re.split(r'\W+', word)
        if s:
            if s[0].strip():
                cleaned_words.append(s[0])
    return cleaned_words


def query_titles(titles):
    """
    Query Wikipedia API with `titles' list and return existent `ex_titles'

    """


def main():
    text = \
    (
        "Researchers at the University of Pittsburgh have published more than "
        "a century's worth of data on scores of infectious diseases they compiled"
        " while putting together computer models and simulations for research."
    )
    print text
    print COMMON_WORDS
