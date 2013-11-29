import json
import math
from Queue import Queue
import re
import requests
import urllib
import urllib2
import urllib3
#import grequests
import string
import time
import threading
from ppp.utils import db
from ppp.utils.decorators import timing
from ppp.settings import IO_BOUND
from .data.settings import (WIKIPEDIA_API_URL, WIKIPEDIA_API_QUERY_PARAMS,
                            COMMON_WORDS, WIKIPEDIA_API_TITLE_LIMIT, TEXT,
                            ENDING_PUNCTUATIONS)


http = urllib3.PoolManager()


NUM_THREADS = IO_BOUND.NUM_THREADS

collection_chunk_size = 10

# Single-word possible titles
single_word_collection = set([])

# All possible (combinations) titles except single-word
collection = set([])

# Candidate queue for multithreading
candidates = Queue()

# All existent titles
candidate_titles = set([])

lock = threading.Lock()


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
    normalized = res['query'].get('normalized', [])
    for page_id in pages:
        if int(page_id) > 0:
            entry_title = pages[page_id]['title']
            #print threading.current_thread()
            #print entry_title
            if entry_title in chunk:
                candidates.put(entry_title)
            else:
                raw_title = ''
                for p in normalized:
                    if p['to'] == entry_title:
                        raw_title = p['from']
                        candidates.put(raw_title)
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


def worker(collection_chunk_slice, thread_id):
    #lock.acquire()
    for chunk in collection_chunk_slice:
        threaded_query_chunk(chunk, False)
    #lock.release()


@timing
def proc():
    threads = []
    collection_chunks = get_collection_chunks(collection,
                                              collection_chunk_size)
    single_collection_chunks = get_collection_chunks(single_word_collection,
                                                     collection_chunk_size)
    #print collection_chunks
    #print 'collection chunks: ', len(collection_chunks)
    #print 'one chunks:', len(collection_chunks[0])
    #print single_collection_chunks
    chunksize = int(math.ceil(len(collection_chunks) / float(NUM_THREADS)))
    #print chunksize
    for i in range(NUM_THREADS):
        start = chunksize * i
        end = chunksize * (i + 1)
        if i == NUM_THREADS - 1:
            end = len(collection_chunks)
        #print start, end
        t = threading.Thread(
            target=worker,
            args=(collection_chunks[start:end], i,)
        )
        threads.append(t)
        t.start()
        #time.sleep(0.1)

    for t in threads:
        t.join()


def urllib2_get_json(url, params):
    query_string = '?'
    for p in params:
        query_string += "%s=%s&" % (p, params[p])

    full_url = url + '?' + urllib.urlencode(params)
    #print full_url
    #print full_url
    #f = urllib2.urlopen(full_url)
    f = http.request('GET', full_url)
    #return json.loads(f.read())
    return json.loads(f.data)


@timing
def main():
    import time
    #print text
    semantic_parse(TEXT)
    #query_collection(collection, single_word_collection)
    proc()
    #candidates.join()
    #print candidates.qsize()
    #time.sleep(1)
    try:
        while True:
            candidate_titles.add(candidates.get(False))
    except:
        pass
    #print collection
    #print single_word_collection
    #print candidate_titles
    db.write_list_to_lines("io_bound-output_mt.txt", list(candidate_titles))
    #print res
    #print COMMON_WORDS
