#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License;
# you may not use this file except in compliance with the Elastic License.
#

import argparse
import subprocess
import glob
import os
import shutil
import sys

ECS_SCRIPT = 'scripts/generator.py'
GEN_ECS_FLAT = 'generated/ecs/ecs_flat.yml'


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('ecs', help='path to the root directory of the ecs project')
    parser.add_argument('custom_schema', help='path to custom schema directory')
    parser.add_argument('subset', nargs='+', help='one or more glob style directories of subset definitions')
    parser.add_argument('out', help='directory to store the generated files')
    parser.add_argument('--ecs_git_ref', help='github reference tag or hash version')
    parser.add_argument('--out-schema-dir', help='directory to copy the generated example files')

    return parser.parse_args()


def generate_subset(ecs_path, custom_schema, subset_file, out, ecs_git_ref):
    subset_out = os.path.join(os.path.abspath(out), os.path.splitext(os.path.basename(subset_file))[0])
    print('Generating subset fields for: {}'.format(subset_file))
    ret = subprocess.run(['python', ECS_SCRIPT, '--include', os.path.abspath(custom_schema),
                          '--subset', os.path.abspath(subset_file),
                          '--out', subset_out, '--ref', ecs_git_ref], stdout=subprocess.PIPE, check=True,
                         cwd=ecs_path, universal_newlines=True)
    print('Generation output-----------------')
    for line in ret.stdout.splitlines():
        print(line,)
    print('Finished generating subset-----------------')


def create_event_schema(subset, out, out_schema_dir):
    subset_basename = os.path.basename(subset)
    subset_no_ext = os.path.splitext(subset_basename)[0]
    abs_out = os.path.abspath(out)
    abs_out_schema_dir = os.path.abspath(out_schema_dir)
    example = os.path.join(abs_out_schema_dir, subset_basename)
    flat_ecs = os.path.join(abs_out, subset_no_ext, GEN_ECS_FLAT)

    print('Copy generated example file [{}] to {}'.format(subset_basename, abs_out_schema_dir))
    shutil.copy(flat_ecs, example)


def get_glob_files(paths):
    all_files = []
    for path in paths:
        all_files.extend(glob.glob(path))

    return all_files


def main():
    if sys.version_info[0] < 3 or sys.version_info[1] < 7:
        raise Exception("Must be using Python 3.7.x or greater, your version: {}.{}".format(
            sys.version_info[0], sys.version_info[1]))

    args = argument_parser()

    print('ecs: {}'.format(args.ecs))
    print('custom_schema: {}'.format(args.custom_schema))
    print('subset: {}'.format(args.subset))
    print('out: {}'.format(args.out))
    print(f'ecs_git_ref: {args.ecs_git_ref}')
    args.out_schema_dir = args.out_schema_dir or args.out
    print('out_schema_dir: {}'.format(args.out_schema_dir))

    subset_files = get_glob_files(args.subset)
    print('Found subset files: {}'.format(subset_files))

    for s in subset_files:
        generate_subset(args.ecs, args.custom_schema, s, args.out, args.ecs_git_ref)
        create_event_schema(s, args.out, args.out_schema_dir)


if __name__ == '__main__':
    main()
