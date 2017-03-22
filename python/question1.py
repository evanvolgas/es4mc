"""
Question 1: How many Green cards with have a subtype of Elf have cmc greater than 2?

Usage:
    question1.py
"""
import sys
sys.path.append('../')

from es import es_client

from docopt import docopt

QUERY_BODY = {
    'query': {
        'bool': {
            'must': [
                {'match': {'colors': 'Green'}},
                {'match': {'subtypes': 'Elf'}},
                {'range': {
                    'cmc': {
                        'gte': 2
                    }
                }
                }
            ]
        }
    }
}

INDEX_NAME = 'mtg'


def run(args):
    es = es_client()

    # ensure the index template is in place
    results = es.search(index=INDEX_NAME, doc_type='cards', body=QUERY_BODY)

    print(results['hits']['total'])


if __name__ == '__main__':
    args = docopt(__doc__)
    run(args)
