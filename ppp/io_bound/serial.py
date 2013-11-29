import re
import requests
from ppp.utils import db
from ppp.utils.decorators import timing
from .data.settings import (WIKIPEDIA_API_URL, WIKIPEDIA_API_QUERY_PARAMS,
                            COMMON_WORDS, WIKIPEDIA_API_TITLE_LIMIT)

single_word_collection = []
candidate_titles = []


def semantic_parse(text):
    global single_word_collection
    raw_words = text.split()
    num_raw_words = len(raw_words)
    single_word_collection = get_single_words(raw_words)
    for i in range(num_raw_words):
        start_index = i
        end_index = num_raw_words
        titles = word_parse(start_index, end_index, raw_words)
        candidate_titles += titles


def word_parse(start_index, end_index, raw_words):
    # Collection of titles
    collection = []
    for j in range(start_index + 1, end_index + 1):
        # Check single-word title
        if j - start_index == 1:
            word = raw_words[start_index]
            if (word.lower() in COMMON_WORDS
                    and word in single_word_collection):
                continue
        title = ' '.join(raw_words[start_index:j])
        collection.append(title.capitalize())
    return collection


def get_single_words(raw_words):
    """Get a list of cleaned single words"""
    cleaned_words = clean_words(raw_words)
    collection = [
        word for word in cleaned_words if word.lower() not in COMMON_WORDS
    ]
    return collection


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


def query_titles(collection, single_word=False):
    """
    Query Wikipedia API with `collection' list and return existent `titles'
    Limit for number of titles per query is 50.

    """
    assert(len(collection)) < WIKIPEDIA_API_TITLE_LIMIT
    params = WIKIPEDIA_API_QUERY_PARAMS
    params['titles'] = '|'.join(collection)
    # Enable `redirects` for single words to avoid counting meaninglessness
    if single_word:
        params['redirects'] = ''
    res = requests.get(WIKIPEDIA_API_URL, params=params).json()
    pages = res['query']['pages']
    normalized = res['query']['normalized']
    titles = []
    for page_id in pages:
        if int(page_id) > 0:
            entry_title = pages[page_id]['title']
            raw_title = ''
            for p in normalized:
                if p['to'] == entry_title:
                    raw_title = p['from']
                    titles.append(raw_title)
                    break
    return titles


def proc():
    pass


def main():
    text = \
    (
        "Researchers at the University of Pittsburgh have published more than "
        "a century's worth of data on scores of infectious diseases they compiled"
        " while putting together computer models and simulations for research."
    )
    print text
    semantic_parse(text)
    #print res
    #print COMMON_WORDS
