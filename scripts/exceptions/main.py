#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License;
# you may not use this file except in compliance with the Elastic License.
#

import argparse
import yaml
import json
import glob


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('schema', help='path to the schema to parse')

    return parser.parse_args()

def main():
    args = argument_parser()
    exceptionable_fields = []
    subset_dirs = glob.glob(args.schema + '/generated/ecs/subset/*')
    for subset in subset_dirs:
        with open(subset + '/ecs_flat.yml') as f:
            flat = yaml.safe_load(f)
        for (field, options) in flat.items():
            if 'exceptionable' in options:
                exceptionable_fields.append(field)
                if 'multi_fields' in options:
                    for multi_field in options['multi_fields']:
                        exceptionable_fields.append(multi_field['flat_name'])
        if exceptionable_fields:
            with open(subset + '/exceptionable.json', 'w') as output:
                json.dump(exceptionable_fields, output, indent=2)

if __name__ == '__main__':
    main()
