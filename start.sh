#!/bin/bash
set -e

# Remove any pre-existing ES data
rm -rf esdata/*

docker build -t es .

echo "Docker image built"

docker run \
    -d \
    -p 19200:9200 \
    -p 15601:5601  \
    --name es4mc \
    -v "$(pwd -P)/esdata":/home/elasticsearch/elasticsearch/data \
    -v "$(pwd -P)/files/wn_s.pl":/home/elasticsearch/elasticsearch/config/wn_s.pl \
    -v "$(pwd -P)/config/elasticsearch.yml":/home/elasticsearch/elasticsearch/config/elasticsearch.yml \
    -v "$(pwd -P)/config/logging.yml":/home/elasticsearch/elasticsearch/config/logging.yml \
    --memory="4g" \
    -e ES_HEAP_SIZE=2g \
    es

echo "Docker container launched"

echo "Sleeping, to let Elasticsearch start up"
sleep 30

echo "Install Elasticsearch Python client library"
pip install -r requirements.txt

echo "Indexing MTG data"
python mtg.py
