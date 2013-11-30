import re
import string
from .data.settings import (WIKIPEDIA_API_TITLE_LIMIT, COMMON_WORDS,
                            ENDING_PUNCTUATIONS)


def get_collection(sentence, single_word_collection):
    """Get collection"""
    collection = set([])
    raw_words = sentence.split()
    num_raw_words = len(raw_words)
    for i in range(num_raw_words):
        start_index = i
        end_index = num_raw_words
        word_parse(start_index, end_index, raw_words, collection,
                   single_word_collection)
    return collection


def get_single_word_collection(sentence):
    """Get a collection of cleaned single words"""
    raw_words = sentence.split()
    cleaned_words = clean_words(raw_words)
    collection = [
        word for word in cleaned_words
        if word.lower() not in COMMON_WORDS
        and word.lower() not in list(string.ascii_lowercase)
        and not word.isdigit()
    ]
    return set(collection)


def word_parse(start_index, end_index, raw_words, collection,
               single_word_collection):
    """
    Parse `raw_words' and generate all possible combinations.
    Store combinations in `collection'.

    """
    for j in range(start_index + 1, end_index + 1):
        # Check single-word titles
        if j - start_index == 1:
            word = raw_words[start_index]
            if (word.lower() in COMMON_WORDS
                    or word.lower() in list(string.ascii_lowercase)
                    or word in single_word_collection
                    or word.isdigit()):
                continue

        title = ' '.join(raw_words[start_index:j])
        pattern = r"([a-zA-Z0-9_ -]+)(%s)$" % "|".join(ENDING_PUNCTUATIONS)
        m = re.search(pattern, title)
        if m:
            cleaned_title = m.group(1)
            collection.add(cleaned_title)
        collection.add(title)


def clean_words(words):  # common (utils)
    """
    Clean words by removing apostrophes, commas, periods, quotation marks, etc.

    """
    cleaned_words = []
    for word in words:
        s = _clean_word(word)
        if s:
            cleaned_words.append(s)
    return cleaned_words


def _clean_word(raw_string):  # common (utils, put this inline in clean_words)
    s = re.split(r'[^a-zA-Z0-9_-]+', raw_string)
    if s:
        if s[0].strip():
            return s[0]


def get_collection_chunks(collection, collection_chunk_size):  # common (pre)
    c = list(collection)
    chunks = [
        c[x: x + collection_chunk_size]
        for x in xrange(0, len(c), collection_chunk_size)
    ]
    return chunks


def get_collection_chunk_size(sentence):  # common (pre)
    """Calculate a most appropriate chunk size"""
    m = 8192 / len(sentence)
    if m > WIKIPEDIA_API_TITLE_LIMIT:
        collection_chunk_size = WIKIPEDIA_API_TITLE_LIMIT
    else:
        collection_chunk_size = m
    return collection_chunk_size
