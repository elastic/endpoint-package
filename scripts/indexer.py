import sys
import json
import copy
import uuid
import argparse

from elasticsearch import Elasticsearch
from random import choice

# WARNING: implicit relative import lives here!
from converter import rekey_alert

def generate_endpoint():

    return {
        "@timestamp":1581457054398,
        "event":{
            "created":"2020-02-11T21:37:34.398Z"
        },
        "endpoint":{
            "policy":{
                "id":"C2A9093E-E289-4C0A-AA44-8C32A414FA7A"
            }
        },
        "agent":{
            "version":"6.5.3",
            "id": str(uuid.uuid4())
        },
        "host":{
            "id": str(uuid.uuid4()),
            "hostname":"pace-7.example.com",
            "ip":[
                "10.25.23.62",
                "10.130.111.203",
                "10.141.84.41"
            ],
            "mac":[
                "fc-7a-ba-34-52-48",
                "a2-2b-eb-cb-b1-7f",
                "ea-d9-7a-97-80-7c"
            ],
            "architecture":"x86_64",
            "os":{
                "name":"windows 6.3",
                "full":"Windows Server 2012R2",
                "version":"6.3"
            }
        }
    }


def special_conversion(old_alert, new_alert):
    services = old_alert.get('endgame', {}).get('data', {}).get('alert_details', {}).get('acting_process', {}).get('services', [])
    for val in services:
        new_alert.setdefault('process', {}).setdefault('services', []).append(val['name'])
    for key, val in old_alert.items():
        if key not in ['endgame', 'labels', 'event']:
            new_alert[key] = val
    new_alert.setdefault('event', {})['kind'] = 'alert'
    new_alert['event']['category'] = 'malware'
    new_alert['event']['module'] = 'endpoint'
    new_alert['event']['dataset'] = 'endpoint'
    event_type_map = {
        'creation': 'creation',
        'open': 'access',
        'execution': 'start',
        'rename': 'change'
    }
    event_type = event_type_map.get(new_alert['event']['action'], None)
    if event_type:
        new_alert['event']['type'] = event_type
    new_alert['agent']['type'] = 'endpoint'



def read_alerts(filename, rekey_mapping):
    with open(filename) as f:
        source_archive = f.read()
        lines = source_archive.splitlines()
        new_alert = {}
        new_alerts = []
        alert = ''
        last_line = ''
        for line in lines:
            alert += line
            if line.strip() == '' and last_line.strip() == '}':
                source_alert = json.loads(alert)['value']['source']
                if source_alert['endgame']['metadata']['key'] == 'fileClassificationEventResponse':
                    rekey_alert(copy.deepcopy(source_alert['endgame']), new_alert, rekey_mapping)
                    special_conversion(source_alert, new_alert)
                    new_alerts.append(new_alert)
                alert = ''
                new_alert = {}
            last_line = line
        return new_alerts


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('es_mapping', type=str, help='the filename of the elasticsearch mapping to use when indexing documents')
    parser.add_argument('source_docs', type=str, help='the filename of the source documents to remap and index')
    parser.add_argument('rekey_mapping', type=str, help='the filename of the mapping to use to rekey the source documents')
    parser.add_argument('--username', type=str, help='elasticsearch username')
    parser.add_argument('--password', type=str, help='elasticsearch password')
    parser.add_argument('--index_name', action='store', help='name of the index to use in elasticsearch')
    return parser.parse_args()


def main(argv):
    index_name = 'my-index'
    username = 'elastic'
    password = 'changeme'
    args = argument_parser()

    if args.index_name:
        index_name = args.index_name
    if args.username:
        username = args.username
    if args.password:
        password = args.password

    es = Elasticsearch(http_auth=(username, password))
    with open(args.es_mapping) as f:
        es_mapping = json.load(f)
        # this will destroy your index indiscriminately so don't screw up the name
        es.indices.delete(index_name, ignore=404)
        es.indices.create(index=index_name, body=es_mapping)

    rekey_mapping = {}
    with open(args.rekey_mapping) as f:
        rekey_mapping = json.load(f)

    endpoints = [generate_endpoint() for i in range(10)]
    endpoint_ids = [end['host']['id'] for end in endpoints]

    alerts = read_alerts(args.source_docs, rekey_mapping)
    for alert in alerts:
        alert['host']['id'] = choice(endpoint_ids)
        alert['event']['id'] = str(uuid.uuid4())
        es.index(index=index_name, body=alert)

    for endpoint in endpoints:
        es.index(index=index_name, body=endpoint)

# usage: indexer.py [-h] [--username USERNAME] [--password PASSWORD]
#                  [--index_name INDEX_NAME]
#                  es_mapping source_docs rekey_mapping
# example usage: python3 indexer.py template.json data.json mapping.json
# template.json is the elasticsearch index mapping
# data.json contains alerts in the schema that the SMP used to stream to elasticsearch
# mapping.json contains a conversion template from the SMP format to the new ECS-centric format
# username and password are optional -- these are for ES authentication
if __name__ == "__main__":
    main(sys.argv[1:])
