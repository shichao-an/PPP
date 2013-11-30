import json
import math
import Queue
import re
import requests
import urllib
import urllib2
import urllib3
#import grequests
import string
import time
import threading
import multiprocessing
from ppp.utils import db
from ppp.utils.decorators import timing
from ppp.settings import IO_BOUND
from .data.settings import (WIKIPEDIA_API_URL, WIKIPEDIA_API_QUERY_PARAMS,
                            COMMON_WORDS, WIKIPEDIA_API_TITLE_LIMIT, TEXT,
                            ENDING_PUNCTUATIONS)

#from .collections import single_word_collection, collection

http = urllib3.PoolManager()


NUM_THREADS = IO_BOUND.NUM_THREADS

collection_chunk_size = 10

# Single-word possible titles
single_word_collection = set([])

# All possible (combinations) titles except single-word
collection = set([])
cq = Queue.Queue()
scq = Queue.Queue()
# Candidate Queue.queue for multithreading
candidates = Queue.Queue()
single_candidates = Queue.Queue()
q = Queue.Queue()

# All existent titles
candidate_titles = set([])
qq = set([])

lock = threading.Lock()

count = 0


def threaded_query_chunk(chunk, single_word=False):
    """
    Query Wikipedia API with a `chunk' of `collection' and generate
    existent titles. Store titles in `candidate_titles'.

    Limit for number of titles per query is 50.

    """
    assert(len(chunk)) <= WIKIPEDIA_API_TITLE_LIMIT
    params = WIKIPEDIA_API_QUERY_PARAMS
    print 'chunk_len:',len(chunk)
    #print threading.current_thread()
    #print len('|'.join(chunk))
    params['titles'] = '|'.join(chunk)
    #print 'title_len:',len(params['titles'])
    # Enable `redirects` for single words to avoid counting meaninglessness
    if single_word:
        params['redirects'] = ''

    #lock.acquire()
    res = urllib2_get_json(WIKIPEDIA_API_URL, params)
    #res = requests.get(WIKIPEDIA_API_URL, params=params).json()
    

    #print res
    pages = res['query']['pages']
    print 'pages_len:', len(pages)
    global count
    print 'count:', count
    normalized = res['query'].get('normalized', [])
    for page_id in pages:
        if int(page_id) > 0:
            entry_title = pages[page_id]['title']
            #print threading.current_thread()
            #print entry_title
            if entry_title in chunk:
                print 'ss-',entry_title
                if entry_title == u'the United States':
                    print '-->', entry_title
                candidates.put(entry_title)
                count += 1
            else:
                raw_title = ''
                for p in normalized:
                    if p['to'] == entry_title:
                        raw_title = p['from']
                        print 'ss-',raw_title
                        if raw_title == u'the United States':
                            print '-->', entry_title
                        candidates.put(raw_title)
                        count += 1
                        break
    #lock.release()

def query_collection(collection, single_word_collection):
    """Query all titles in the `collection' and `single_word_collection'"""
    chunks = get_collection_chunks(collection, collection_chunk_size)
    #print len(chunks)
    for chunk in chunks:
        threaded_query_chunk(chunk)

    #for chunk in single_chunks:
        #threaded_query_chunk(chunk, single_word=True)


def worker(queue, candidates, single_word=False):
        while True:
            try:
                chunk = queue.get(False)
            except Queue.Empty:
                if single_word:
                    print 'SINGLE EMPTY!!!'
                else:
                    print 'EMPTY!!!'
                break

            assert(len(chunk)) <= WIKIPEDIA_API_TITLE_LIMIT
            params = WIKIPEDIA_API_QUERY_PARAMS
            print 'chunk_len:',len(chunk)
            #print threading.current_thread()
            #print len('|'.join(chunk))
            params['titles'] = '|'.join(chunk)
            #print 'title_len:',len(params['titles'])
            # Enable `redirects` for single words to avoid counting meaninglessness
            if single_word:
                params['redirects'] = ''
            res = urllib2_get_json(WIKIPEDIA_API_URL, params)
            #res = requests.get(WIKIPEDIA_API_URL, params=params).json()
            

            #print res

            pages = res['query']['pages']
            print 'pages_len:', len(pages)
            global count
            print 'count:', count

            normalized = res['query'].get('normalized', [])
            #count += len(normalized)

            print '--normalized:', len(normalized)

            for page_id in pages:
                if int(page_id) > 0:
                    entry_title = pages[page_id]['title']
                    if entry_title in chunk:
                        candidates.put(entry_title)
                        count += 1
                        q.put(page_id)
                    else:
                        raw_title = ''
                        for p in normalized:
                            if p['to'] == entry_title:
                                raw_title = p['from']
                                candidates.put(raw_title)
                                q.put(page_id)
                                count += 1
                                break


@timing
def proc():
    threads = []
    collection_chunks = get_collection_chunks(collection,
                                              collection_chunk_size)
    single_collection_chunks = get_collection_chunks(single_word_collection,
                                                     collection_chunk_size)

    chunksize = int(math.ceil(len(collection_chunks) / float(NUM_THREADS)))
    #print chunksize
    """
    for i in range(NUM_THREADS):
        start = chunksize * i
        end = chunksize * (i + 1)
        if i == NUM_THREADS - 1:
            end = len(collection_chunks)
        #print start, end
        t = threading.Thread(
            target=worker,
            args=(collection_chunks[start:end],)
        )
        threads.append(t)
        t.start()
        #time.sleep(1)


    for chunk in collection_chunks:
        t = threading.Thread(
            target=worker,
            args=(chunk,)
        )
        threads.append(t)
        t.start()

    for chunk in single_collection_chunks:
        t = threading.Thread(
            target=worker,
            args=(chunk, True)
        )
        threads.append(t)
        t.start()

    """
    for chunk in collection_chunks:
        cq.put(chunk)
    for chunk in single_collection_chunks:
        scq.put(chunk)
    print 'scq', scq.qsize()
    pool = [
        threading.Thread(target=worker, args=(cq, candidates, False,)) for i in range(4)
    ]

    for t in pool:
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    worker(scq, single_candidates,True)


def request_json(url, params):
    """
    Alternative to requests.get(url, params).json() using urllib3.
    requests is not thread-safe

    """
    encoded = url + '?' + urllib.urlencode(params)
    f = http.request('GET', full_url)
    return json.loads(f.data)


@timing
def main():
    import time
    #print text
    semantic_parse(TEXT)
    #query_collection(collection, single_word_collection)
    proc()
    print 'count:',count
    #candidates.join()
    print 'cand:', candidates.qsize()
    print 'single cand:', single_candidates.qsize()
    print q.qsize()
    #time.sleep(1)
    try:
        while True:
            candidate_titles.add(candidates.get(False))
    except:
        pass
    try:
        while True:
            #print single_candidates.get(False)
            candidate_titles.add(single_candidates.get(False))
    except:
        pass
    print len(candidate_titles)
    try:
        while True:
            qq.add(q.get(False))
    except:
        pass
    #print collection
    #print single_word_collection
    #print candidate_titles
    db.write_list_to_lines("io_bound-output_mt.txt", list(candidate_titles))
    #print res
    #print COMMON_WORDS
