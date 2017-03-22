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

NEW_FIELDS = {
    'blue_cost': {
        'type': 'integer'
    },
    'red_cost': {
        'type': 'integer'
    },
    'green_cost': {
        'type': 'integer'
    },
    'black_cost': {
        'type': 'integer'
    },
    'white_cost': {
        'type': 'integer'
    },
    'generic_cost': {
        'type': 'integer'
    }
}

COLOR_COSTS_MAP = {
    'blue_cost': '{U}',
    'red_cost': '{R}',
    'green_cost': '{G}',
    'black_cost': '{B}',
    'white_cost': '{W}',
}


def run(args):
    es = es_client()

    # don't hate me because I'm mutable
    INDEX_MAPPINGS['mappings']['cards']['properties'].update(NEW_FIELDS)

    if es.indices.exists(INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
        idx = merge_two_dicts(INDEX_MAPPINGS, INDEX_SETTINGS)
        es.indices.create(index=INDEX_NAME, body=idx)

    card_iter = helpers.scan(es, index='mtg')

    helpers.bulk(es, enriched_card_iter(card_iter))


def get_color_mana_costs(mana_cost):
    """Get a dict that maps the color key to its cost"""
    mana_costs = {}
    for key in COLOR_COSTS_MAP.keys():
        mana_costs[key] = mana_cost.count(COLOR_COSTS_MAP[key])

    return mana_costs


def get_generic_cost(card_data, mana_costs):
    """Compute the generic cost as the difference of the difference of
     cmc and the sum of the color costs"""
    color_cost_sum = sum([cost for cost in mana_costs.values()])

    return {'generic_cost': int(card_data['_source']['cmc']) - color_cost_sum}


def enrich_card(card_data):
    """Enrich a card with the color cost data"""
    enriched_card = deepcopy(card_data)
    enriched_card['_index'] = INDEX_NAME

    mana_costs = get_color_mana_costs(card_data['_source']['manaCost'])
    mana_costs.update(get_generic_cost(card_data, mana_costs))

    enriched_card['_source'].update(mana_costs)

    return merge_two_dicts(enriched_card, mana_costs)


def enriched_card_iter(card_iter):
    """Generator into enriched cards"""
    for card in card_iter:
        try:
            yield enrich_card(card)
        except KeyError:
            continue

if __name__ == '__main__':
    args = docopt(__doc__)
    run(args)
