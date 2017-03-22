from __future__ import print_function

import json
import re

from datetime import datetime

from elasticsearch import Elasticsearch, helpers

from index_settings import INDEX_MAPPINGS, INDEX_SETTINGS
from util import merge_two_dicts

FILE = "AllCards.json"

ES_HOST = ['127.0.0.1:19200']

CLIENT = Elasticsearch(hosts=ES_HOST, timeout=120)

INDEX_NAME = 'mtg'
TYPE_NAME = "cards"
REPLACE_KEYS = ["power", "toughness"]

idx = merge_two_dicts(INDEX_SETTINGS, INDEX_MAPPINGS)

with open(FILE) as motg_data:
    data = json.load(motg_data)

# CREATE YOUR BULK REQUEST
bulk_data = []
for k, v in data.items():
    v["@timestamp"] = datetime.now()
    for m in REPLACE_KEYS:
        if v.get(m) and (isinstance(v.get(m), str) or "*" in v.get(m)):
            v[m] = re.sub('[^0-9]', '', v[m])
    op_dict = {
        "_op_type": "index",
        "_index": INDEX_NAME,
        "_type": TYPE_NAME,
        "_id": k,
    }
    d = merge_two_dicts(op_dict, v)
    bulk_data.append(d)


# CREATE/RESET THE INDEX
if CLIENT.indices.exists(INDEX_NAME):
    print("deleting '%s' index..." % (INDEX_NAME))
    res = CLIENT.indices.delete(index=INDEX_NAME)
    print(" response: '%s'" % (res))


print("creating '%s' index..." % (INDEX_NAME))
res = CLIENT.indices.create(index=INDEX_NAME, body=idx)
print(" response: '%s'" % (res))


# INDEX THE DATA
print("bulk indexing...")
for success, info in helpers.parallel_bulk(CLIENT, bulk_data):
    if not success:
        print('A document failed:', info)
