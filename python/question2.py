"""
Question 2: Write an aggregation that shows the average power as a histogram over cmc. The value
of cmc seems small, so use use an interval of 1 point (I don't advise doing this in Kibana).
What happens? Why are the results a little unwieldy? What could you do fix it?

Usage:
    question2.py
"""
import sys

from es import es_client

sys.path.append('../')

from docopt import docopt

INDEX_NAME = 'mtg'

AGGREGATION = {}


def run(args):
    es = es_client()

    results = es.search(index=INDEX_NAME, doc_type='cards', body=AGGREGATION)

    print(results)


if __name__ == '__main__':
    args = docopt(__doc__)
    run(args)
