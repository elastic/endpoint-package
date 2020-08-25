#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License;
# you may not use this file except in compliance with the Elastic License.
#

import argparse

import yaml
from yamlinclude import YamlIncludeConstructor


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-base_dir', help='base directory for the included yaml files')
    parser.add_argument('-field_template_file', help='the template file to use for the merge')
    parser.add_argument('-output_file', help='the file to dump output')
    return parser.parse_args()


def main():
    args = argument_parser()

    print('base_dir: {}'.format(args.base_dir))
    print('field_template_file: {}'.format(args.field_template_file))
    print('output_file: {}'.format(args.output_file))

    YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader, base_dir=args.base_dir)

    with open(args.field_template_file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        
    with open(args.output_file, 'w') as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False)


if __name__ == '__main__':
    main()
