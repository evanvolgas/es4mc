"""
Question 3: Scan all of the cards and reindex them into a new index adding new fields that contain the mana cost
for each color as well as the generic cost.

Usage:
    question3.py
"""
import sys
sys.path.append('../')

from copy import deepcopy

from docopt import docopt
from elasticsearch import helpers

from es import es_client
from index_settings import INDEX_MAPPINGS, INDEX_SETTINGS
from util import merge_two_dicts

BATCH_SIZE = 500

INDEX_NAME = 'mtg-color-cost'


def run(args):
    es = es_client()

    # do some stuff


if __name__ == '__main__':
    args = docopt(__doc__)
    run(args)
