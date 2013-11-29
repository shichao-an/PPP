import os
from ppp.utils import db

CURRENT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
WIKIPEDIA_API_URL = "http://en.wikipedia.org/w/api.php"
WIKIPEDIA_API_QUERY_PARAMS = {
    "action": "query",
    "format": "json",
    "titles": "",
}
WIKIPEDIA_API_TITLE_LIMIT = 50
COMMON_WORDS = db.read_lines_to_list(os.path.join(CURRENT_PATH, "common.txt"))
TEXT = db.read_to_string(os.path.join(CURRENT_PATH, "text.txt"))
ENDING_PUNCTUATIONS = [";", ",", "\.", "'", "'s", "'d", "'ll", "'m"]
