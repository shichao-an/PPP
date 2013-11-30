import re
import requests
import string
from ppp.utils import db
from ppp.utils.decorators import timing
from .data.settings import (WIKIPEDIA_API_URL, WIKIPEDIA_API_QUERY_PARAMS,
                            COMMON_WORDS, WIKIPEDIA_API_TITLE_LIMIT, TEXT,
                            ENDING_PUNCTUATIONS)

from .collections import (get_collection, get_single_word_collection,
                          get_collection_chunks, get_collection_chunk_size)


collection = set([])
single_word_collection = set([])
collection_chunk_size = 10
candidate_titles = []
count = 0


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
    print 'chunk_len:',len(chunk)
    res = requests.get(WIKIPEDIA_API_URL, params=params).json()
    #print res
    pages = res['query']['pages']
    print 'page_len:',len(pages)
    global count
    print 'count:', count
    normalized = res['query'].get('normalized', [])
    for page_id in pages:
        if int(page_id) > 0:
            entry_title = pages[page_id]['title']
            if entry_title in chunk:
                candidate_titles.append(entry_title)
                print entry_title
                count += 1
            else:
                raw_title = ''
                for p in normalized:
                    if p['to'] == entry_title:
                        raw_title = p['from']
                        print raw_title
                        candidate_titles.append(raw_title)
                        count += 1
                        break


def set_globals():
    global collection
    global single_word_collection
    global collection_chunk_size
    single_word_collection = get_single_word_collection(TEXT)
    collection = get_collection(TEXT, single_word_collection)
    #print collection
    collection_chunk_size = get_collection_chunk_size(TEXT)


@timing
def proc():
    """Query all titles in `collection' and `single_word_collection'
    after dividing them into chunks.
    """
    #global collection
    #print collection
    chunks = get_collection_chunks(collection, collection_chunk_size)
    for chunk in chunks:
        query_chunk(chunk)
    single_chunks = get_collection_chunks(
        single_word_collection, collection_chunk_size)
    for chunk in single_chunks:
        query_chunk(chunk, single_word=True)


@timing
def main():
    set_globals()
    proc()
    db.write_list_to_lines("io_bound-output_serial.txt", candidate_titles)

