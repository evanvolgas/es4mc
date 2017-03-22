"""
Question 2: How many cards have a 'text' field that contains the words 'counter' or 'Counter'?

Usage:
    question2.py
"""
import sys

from es import es_client

sys.path.append('../')

from docopt import docopt
from elasticsearch import helpers

INDEX_NAME = 'mtg'


def run(args):
    es = es_client()

    # do stuff here :)


if __name__ == '__main__':
    args = docopt(__doc__)
    run(args)
