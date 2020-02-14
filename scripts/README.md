indexer.py usage: indexer.py [-h] [--username USERNAME] [--password PASSWORD]
                  [--index_name INDEX_NAME]
                  es_mapping source_docs rekey_mapping

example usage: python3 indexer.py template.json data.json mapping.json

The indexer.py script takes in a set of alerts in the old SMP format dumped from evrelay, converts them to the proposed ECS alert format, and indexes them in Elasticsearch. The structure of mapping.json follows the structure of the old SMP alert schema and for each old field provides a new field name.