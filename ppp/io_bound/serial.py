import re
import requests
import string
from ppp.utils import db
from ppp.utils.decorators import timing
from .data.settings import (WIKIPEDIA_API_URL, WIKIPEDIA_API_QUERY_PARAMS,
                            COMMON_WORDS, WIKIPEDIA_API_TITLE_LIMIT, TEXT,
                            ENDING_PUNCTUATIONS)

collection_chunk_size = 10

# Single-word possible titles
single_word_collection = set([])

# All possible (combinations) titles except single-word
collection = set([])

# All existent titles
candidate_titles = []


def semantic_parse(sentence):
    global single_word_collection
    set_collection_chunk_size(sentence)
    raw_words = sentence.split()
    num_raw_words = len(raw_words)
    single_word_collection = get_single_words(raw_words)
    for i in range(num_raw_words):
        start_index = i
        end_index = num_raw_words
        word_parse(start_index, end_index, raw_words)


def word_parse(start_index, end_index, raw_words):
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


def get_single_words(raw_words):
    """Get a list of cleaned single words"""
    cleaned_words = clean_words(raw_words)
    collection = [
        word for word in cleaned_words
        if word.lower() not in COMMON_WORDS
        and word.lower() not in list(string.ascii_lowercase)
        and not word.isdigit()
    ]
    return collection


def clean_words(words):
    """
    Clean words by removing apostrophes, commas, periods, quotation marks, etc.

    """
    cleaned_words = []
    for word in words:
        s = clean_word(word)
        if s:
            cleaned_words.append(s)
    return cleaned_words


def clean_word(raw_string):
    s = re.split(r'[^a-zA-Z0-9_-]+', raw_string)
    if s:
        if s[0].strip():
            return s[0]


def query_chunk(chunk, single_word=False):
    """
    Query Wikipedia API with a `chunk' of `collection' and generate
    existent titles. Store titles in `candidate_titles'.

    Limit for number of titles per query is 50.

    """
    assert(len(chunk)) <= WIKIPEDIA_API_TITLE_LIMIT
    params = WIKIPEDIA_API_QUERY_PARAMS
    #print len(chunk)
    #print len('|'.join(chunk))
    params['titles'] = '|'.join(chunk)
    # Enable `redirects` for single words to avoid counting meaninglessness
    if single_word:
        params['redirects'] = ''
    res = requests.get(WIKIPEDIA_API_URL, params=params).json()
    #print res
    pages = res['query']['pages']
    normalized = res['query'].get('normalized', [])
    for page_id in pages:
        if int(page_id) > 0:
            entry_title = pages[page_id]['title']
            if entry_title in chunk:
                candidate_titles.append(entry_title)
            else:
                raw_title = ''
                for p in normalized:
                    if p['to'] == entry_title:
                        raw_title = p['from']
                        candidate_titles.append(raw_title)
                        break


def query_collection(collection, single_word_collection):
    """Query all titles in the `collection' and `single_word_collection'"""
    chunks = get_collection_chunks(collection, collection_chunk_size)
    print len(chunks)
    for chunk in chunks:
        query_chunk(chunk)
    single_chunks = get_collection_chunks(single_word_collection,
                                          collection_chunk_size)
    for chunk in single_chunks:
        query_chunk(chunk, single_word=True)


def get_collection_chunks(collection, collection_chunk_size):
    c = list(collection)
    chunks = [
        c[x: x + collection_chunk_size]
        for x in xrange(0, len(c), collection_chunk_size)
    ]
    return chunks


def set_collection_chunk_size(sentence):
    """Calculate a most appropriate chunk size"""
    global collection_chunk_size
    m = 8192 / len(sentence)
    if m > WIKIPEDIA_API_TITLE_LIMIT:
        collection_chunk_size = WIKIPEDIA_API_TITLE_LIMIT
    else:
        collection_chunk_size = m


@timing
def proc():
    query_collection(collection, single_word_collection)


@timing
def main():
    #print text
    semantic_parse(TEXT)
    proc()
    #print collection
    #print single_word_collection
    #print candidate_titles
    db.write_list_to_lines("io_bound-output_serial.txt", candidate_titles)
    #print res
    #print COMMON_WORDS
