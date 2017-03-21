# ES4MC Night School: MTG Edition
This repo contains the information you will need in order to build a Docker image with Elasticsearch 2.4.4 and Kibana 4.6.4; index the [Magic:The Gathering card data](http://mtgjson.com) into Elasticsearch, and begin querying and exploring the data.

In order to use this repo, there are a few prerequesites:

1. You must have [Docker](https://store.docker.com/editions/community/docker-ce-desktop-mac?tab=description) installed and running
2. You must have Python PIP installed on whatever Python environment you are using. If you're not sure if you have PIP or not, run `which pip` from your terminal. If you need to install Pip, please consult the [Hitchhickers Guide to Python](http://docs.python-guide.org/en/latest/starting/install/osx/).

## Getting started
Once you have ensured that you have both Docker and PIP installed on your computer, you may build your local Elasticsearch/Kibana instance and index the MTG data by running `./start.sh` from your command line.

After you run `./start.sh`, Elasticsearch will be available in your browser at [localhost:19200](http://localhost:19200) and Kibana will be available at [localhost:15601](http://localhost:15601).

The first time you run Kibana, you will need to configure an index pattern. You will see a text box that contains `logstash-*`. Replace that with `mtg` and use `@timestamp` as your Time-field name.

Once you have defined the `mtg` index pattern, click the `Discover` tab near the left hand corner and set the time interval to "Last 1 year."

If you've already run `./start.sh` before and decide you wish to run the `mtg.py` script and reindex the data for some reason (perhaps to use some different mappings, or change the analyzers in some way) you can run the `python mtg.py` instead of running `./start.sh`. The start script builds the docker image and launches a container for ES, which you shouldn't need to do more than once. If you aren't sure if your Docker container is still running, execute `docker ps` in your terminal and see if there is a docker container called `es4mc` that is running.

## A few helpful commands
Once you have launched the Docker container and indexed the data, you can verify that Elasticsearch is running by visiting [localhost:19200](http://localhost:19200).

You can see the index settings and mappings for the MTG data by going to [localhost:19200/mtg](http://localhost:19200/mtg)

You can search the MTG data by going to [localhost:19200/mtg/_search](http://localhost:19200/mtg/_search). You can also execute more complex searches against that endpoint by using `curl` e.g.


```
curl http://localhost:19200/mtg/_search -d '
{
  "size": 5,
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "colors": "Green"
          }
        }
      ],
      "should": [
        {
          "match": {
            "subtype": {
              "query": "Elf",
              "boost": 10
            }
          }
        },
        {
          "match": {
            "type": {
              "query": "elf",
              "boost": 8
            }
          }
        },
        {
          "match": {
            "name": {
              "query": "elf elven elves",
              "boost": 5
            }
          }
        },
        {
          "match": {
            "name.synonym": {
              "query": "elf elven elves",
              "operator": "or",
              "boost": 2
            }
          }
        },
        {
          "match": {
            "name.ngram": {
              "query": "elf",
              "boost": 1
            }
          }
        }
      ],
      "must_not": [
        {
          "term": {
            "colors": "Red"
          }
        }
      ],
      "filter": []
    }
  }
}'
```

Much of the class will be dedicated to the Analysis API, a sample invocation of which is: [http://localhost:19200/mtg/_analyze?text=good&analyzer=synonym](http://localhost:19200/mtg/_analyze?text=good&analyzer=synonym)

The `name` and `text` fields are analyzed five different ways out of the box, including:

1. ngram
2. raw
3. standard
4. snowball
5. synonym

analyzers. There is also an additional analyzer hidden in the index as an easter egg. See if you can find it.

Last, we will make use of the [More Like This](https://www.elastic.co/guide/en/elasticsearch/reference/2.4/query-dsl-mlt-query.html) query in this class. A sample invocation is


```
curl http://localhost:19200/mtg/_search -d
'{
  "query": {
    "more_like_this": {
      "fields": [
        "text.synonym"
      ],
      "like": [
        {
          "_index": "mtg",
          "_type": "cards",
          "_id": "Ambiguity"
        }
      ]
    }
  }
}'
```


## Buyer Beware
We are trying to make sure that this works for as many people as possible with as little hassle as possible. We do include some large files in this repo as well as make a few assumptions about port availability that may not be generic enough for wide spread use. If you see anything you'd like to improve, PRs are most certainly welcome. If you see anything that's broken, please let us know and we'll do our best to fix it before anyone else notices.
