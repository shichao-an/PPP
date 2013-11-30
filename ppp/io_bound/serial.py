import requests
from ppp.utils import db
from ppp.utils.decorators import timing
from .data.settings import (WIKIPEDIA_API_URL, WIKIPEDIA_API_QUERY_PARAMS,
                            WIKIPEDIA_API_TITLE_LIMIT, TEXT)

from .collections import (get_collection, get_single_word_collection,
                          get_collection_chunks, get_collection_chunk_size,
                          get_num_chunks)


collection = set([])
single_word_collection = set([])
collection_chunk_size = 10
candidate_titles = set([])


def query_chunk(chunk, single_word=False):
    """
    Query Wikipedia API with a `chunk' of `collection' and generate
    existent titles. Store titles in `candidate_titles'.

    Limit for number of titles per query is 50.

    """
    assert(len(chunk)) <= WIKIPEDIA_API_TITLE_LIMIT
    params = WIKIPEDIA_API_QUERY_PARAMS

    params['titles'] = '|'.join(chunk)
    # Enable `redirects` for single words to avoid counting meaninglessness
    if single_word:
        params['redirects'] = ''
    res = requests.get(WIKIPEDIA_API_URL, params=params).json()
    pages = res['query']['pages']
    normalized = res['query'].get('normalized', [])
    for page_id in pages:
        if int(page_id) > 0:
            entry_title = pages[page_id]['title']
            if entry_title in chunk:
                candidate_titles.add(entry_title)
            else:
                raw_title = ''
                for p in normalized:
                    if p['to'] == entry_title:
                        raw_title = p['from']
                        candidate_titles.add(raw_title)
                        break


def set_globals():
    global collection, single_word_collection, collection_chunk_size
    single_word_collection = get_single_word_collection(TEXT)
    collection = get_collection(TEXT, single_word_collection)
    collection_chunk_size = get_collection_chunk_size(TEXT)


@timing
def proc():
    """
    Query all titles in `collection' and `single_word_collection'
    after dividing them into chunks.
    """
    collection_chunks = get_collection_chunks(
        collection, collection_chunk_size)
    single_collection_chunks = get_collection_chunks(
        single_word_collection, collection_chunk_size)

    num_chunks = get_num_chunks(collection_chunks, single_collection_chunks)
    print 'HTTP requests: %d' % num_chunks

    for chunk in collection_chunks:
        query_chunk(chunk)
    for chunk in single_collection_chunks:
        query_chunk(chunk, single_word=True)


def main():
    set_globals()
    proc()
    db.write_list_to_lines(
        "io_bound-output_serial.txt", list(candidate_titles))
