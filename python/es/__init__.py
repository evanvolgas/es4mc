import sys
sys.path.append('')

from elasticsearch import Elasticsearch

NETACUITY_HOST = '10.130.64.16'

_netacuity_client = None

ES_HOSTS = {'host': 'localhost', 'port': '19200'}

# We instantiate the ES client at the module level to preserve it across requests
ES_CLIENT = None


def es_client():
    """Connect the ES client if necessary and return the client.

    :return: ES client object
    """
    global ES_CLIENT
    if ES_CLIENT is None:
        ES_CLIENT = Elasticsearch(hosts=[ES_HOSTS])
    return ES_CLIENT
