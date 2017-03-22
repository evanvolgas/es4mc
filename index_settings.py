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
