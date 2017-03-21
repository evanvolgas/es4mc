from __future__ import print_function

import json
import re

from datetime import datetime

from elasticsearch import Elasticsearch, helpers


FILE = "AllCards.json"

ES_HOST = ['127.0.0.1:19200']

CLIENT = Elasticsearch(hosts=ES_HOST, timeout=120)

INDEX_NAME = 'mtg'
TYPE_NAME = "cards"
REPLACE_KEYS = ["power", "toughness"]

INDEX_SETTINGS = {
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 0,
        "index": {
            "analysis": {
                "analyzer": {
                    "mailkimp": {
                        "tokenizer": "whitespace",
                        "filter": [
                            "mailkimp"
                        ]
                    },
                    "ngram": {
                        "tokenizer": "ngram_tokenizer"
                    },
                    "snowball": {
                        "type": "snowball",
                        "language": "English"
                    },
                    "synonym": {
                        "tokenizer": "whitespace",
                        "filter": [
                            "synonym"
                        ]
                    }
                },
                "filter": {
                    "synonym": {
                        "type": "synonym",
                        "format": "wordnet",
                        "synonyms_path": "wn_s.pl"
                    },
                    "mailkimp": {
                        "type": "synonym",
                        "synonyms": [
                                "mailchimp, mailkimp, failchip, kalelimp, mailshrimp, jailblimp, snailprimp, malecrimp, nailchamp, veilhymn => mailchimp, mailkimp, failchip, kalelimp, mailshrimp, jailblimp, snailprimp, malecrimp, nailchamp, veilhymn"
                        ]
                    }
                },
                "tokenizer": {
                    "ngram_tokenizer": {
                        "type": "nGram",
                        "min_gram": "2",
                        "max_gram": "3",
                        "token_chars": [
                            "letter",
                            "digit"
                        ]
                    }
                }
            }
        }
    }
}


INDEX_MAPPINGS = {
    "mappings": {
        "cards": {
            "_all": {
                "enabled": True,
                "omit_norms": True
            },
            "properties": {
                "@timestamp": {
                    "type": "date",
                    "format": "strict_date_optional_time||epoch_millis"
                },
                "cmc": {
                    "type": "long"
                },
                "colorIdentity": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "colors": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "hand": {
                    "type": "long"
                },
                "id": {
                    "type": "string"
                },
                "imageName": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "layout": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "life": {
                    "type": "long"
                },
                "loyalty": {
                    "type": "long"
                },
                "manaCost": {
                    "type": "string",
                },
                "name": {
                    "type": "string",
                    "fields": {
                        "ngram": {
                            "type": "string",
                            "analyzer": "ngram"
                        },
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "simple": {
                            "type": "string",
                            "analyzer": "simple"
                        },
                        "snowball": {
                            "type": "string",
                            "analyzer": "snowball"
                        },
                        "synonym": {
                            "type": "string",
                            "analyzer": "synonym"
                        }
                    }
                },
                "names": {
                    "type": "string"
                },
                "power": {
                    "type": "double"
                },
                "starter": {
                    "type": "boolean"
                },
                "subtypes": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "supertypes": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "text": {
                    "type": "string",
                    "fields": {
                        "ngram": {
                            "type": "string",
                            "analyzer": "ngram"
                        },
                        "simple": {
                            "type": "string",
                            "analyzer": "simple"
                        },
                        "snowball": {
                            "type": "string",
                            "analyzer": "snowball"
                        },
                        "synonym": {
                            "type": "string",
                            "analyzer": "synonym"
                        }
                    }
                },
                "toughness": {
                    "type": "double"
                },
                "type": {
                    "type": "string",
                    "fields": {
                        "raw": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
                },
                "types": {
                    "type": "string",
                    "index": "not_analyzed"
                }
            }
        },
        "_default_": {
            "_all": {
                "enabled": True,
                "omit_norms": True
            }
        }
    }
}


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

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
