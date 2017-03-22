"""
Question 1: How many Green cards with a subtype of Elf have cmc greater than 2?

Usage:
    question1.py
"""
import sys
sys.path.append('../')

from es import es_client

from docopt import docopt

# write the query body
QUERY_BODY = {}

INDEX_NAME = 'mtg'


def run(args):
    es = es_client()

    results = es.search(index=INDEX_NAME, doc_type='cards', body=QUERY_BODY)

    print(results['hits']['total'])


if __name__ == '__main__':
    args = docopt(__doc__)
    run(args)
