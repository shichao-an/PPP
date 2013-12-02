import json
import Queue
import urllib
import urllib3
import threading
from ppp.utils import db
from ppp.utils.decorators import timing
from ppp.settings import IO_BOUND
from .data.settings import (WIKIPEDIA_API_URL, WIKIPEDIA_API_QUERY_PARAMS,
                            WIKIPEDIA_API_TITLE_LIMIT, TEXT)
from .collections import (get_collection, get_single_word_collection,
                          get_collection_chunks, get_collection_chunk_size,
                          get_num_chunks)

NUM_THREADS = IO_BOUND.NUM_THREADS

collection = set([])
single_word_collection = set([])
collection_chunk_size = 10

# Use urllib3 PoolManager for thread-safe HTTP requests
pool_manager = urllib3.PoolManager()

collection_queue = Queue.Queue()
single_collection_queue = Queue.Queue()
candidates = Queue.Queue()

candidate_titles = set([])


def worker(queue, single_word=False):
    """
    Worker thread for querying Wikipedia API with a `chunk' of `collection'
    and generate existent titles. Queue titles in `candidates'.

    Limit for number of titles per query is 50.

    """
    while True:
        try:
            chunk = queue.get(False)
        except Queue.Empty:
            break

        assert(len(chunk)) <= WIKIPEDIA_API_TITLE_LIMIT
        params = WIKIPEDIA_API_QUERY_PARAMS
        params['titles'] = '|'.join(chunk)

        if single_word:
            params['redirects'] = ''
        res = request_json(WIKIPEDIA_API_URL, params)

        pages = res['query']['pages']
        normalized = res['query'].get('normalized', [])
        for page_id in pages:
            if int(page_id) > 0:
                entry_title = pages[page_id]['title']
                if entry_title in chunk:
                    candidates.put(entry_title)
                else:
                    raw_title = ''
                    for p in normalized:
                        if p['to'] == entry_title:
                            raw_title = p['from']
                            candidates.put(raw_title)
                            break


@timing
def proc():
    threads = []
    collection_chunks = get_collection_chunks(
        collection, collection_chunk_size)
    single_collection_chunks = get_collection_chunks(
        single_word_collection, collection_chunk_size)

    num_chunks = get_num_chunks(collection_chunks, single_collection_chunks)
    print 'HTTP requests: %d' % num_chunks
    #print 'Chunk size: %d' % collection_chunk_size

    # Put chunks into queues for the thread pool
    for chunk in collection_chunks:
        collection_queue.put(chunk)
    for chunk in single_collection_chunks:
        single_collection_queue.put(chunk)

    thread_pool = [
        threading.Thread(
            target=worker,
            args=(collection_queue, False)
        ) for i in range(NUM_THREADS)
    ]

    for t in thread_pool:
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Process `single_collection_queue' in the main thread after joining
    # all other worker threads to avoid conflicting with them
    worker(single_collection_queue, single_word=True)


def request_json(url, params):
    """
    Alternative to requests.get(url, params).json() using urllib3.
    requests is not thread-safe

    """
    encoded_url = url + '?' + urllib.urlencode(params)
    f = pool_manager.request('GET', encoded_url)
    return json.loads(f.data)


def set_globals():
    global collection, single_word_collection, collection_chunk_size
    single_word_collection = get_single_word_collection(TEXT)
    collection = get_collection(TEXT, single_word_collection)
    collection_chunk_size = get_collection_chunk_size(TEXT)


@timing
def main():
    set_globals()
    proc()
    try:
        while True:
            candidate_titles.add(candidates.get(False))
    except:
        pass

    db.write_list_to_lines("io_bound-output_mt.txt", list(candidate_titles))
