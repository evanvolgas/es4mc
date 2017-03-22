"""
Question 2: How many cards have a 'text' field that contains the words 'counter' or 'Counter'?

Usage:
    question2_solution.py
"""
import sys

from es import es_client

sys.path.append('../')

from docopt import docopt
from elasticsearch import helpers

QUERY_BODY = {"query": {"match_all": {}}}

INDEX_NAME = 'mtg'


def run(args):
    es = es_client()

    # ensure the index template is in place
    results = es.search(index=INDEX_NAME, doc_type='cards', body=QUERY_BODY)

    card_iter = helpers.scan(es, index=INDEX_NAME)

    count = 0

    for card in card_iter:
        try:
            text = card['_source']['text'].lower()
        except KeyError:
            # some cards don't have text
            continue
        if 'counter' in text:
            count += 1

    print(count)


if __name__ == '__main__':
    args = docopt(__doc__)
    run(args)
