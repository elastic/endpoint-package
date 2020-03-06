import argparse
import subprocess
import glob
import os
import yaml
import re
import shutil
import sys

ECS_SCRIPT = 'scripts/generator.py'
GEN_ECS = 'generated/ecs/ecs_nested.yml'


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('ecs', help='path to the root directory of the ecs project')
    parser.add_argument('custom_schema', help='path to custom schema directory')
    parser.add_argument('subset', nargs='+', help='one or more glob style directories of subset definitions')
    parser.add_argument('out', help='directory to store the generated files')
    parser.add_argument('--out-schema-dir', help='directory to copy the generated example files')

    return parser.parse_args()


def generate_subset(ecs_path, custom_schema, subset_file, out):
    subset_out = os.path.join(os.path.abspath(out), os.path.splitext(os.path.basename(subset_file))[0])
    print('Generating subset fields for: {}'.format(subset_file))
    ret = subprocess.run(['python', ECS_SCRIPT, '--include', os.path.abspath(custom_schema),
                          '--subset', os.path.abspath(subset_file),
                          '--out', subset_out], stdout=subprocess.PIPE, check=True,
                         cwd=ecs_path, universal_newlines=True)
    print('Generation output-----------------')
    for line in ret.stdout.splitlines():
        print(line,)
    print('Finished generating subset-----------------')


def gen_fields_from_dots(keys, schema):
    if len(keys) == 1:
        return {
            keys[0]: schema
        }
    else:
        return {
            keys[0]: {
                'fields': gen_fields_from_dots(keys[1:], schema)
            }
        }


def merge(a, b, path=None):
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


def expand_dots(nested_yaml):
    merged = {}
    for key, schema in nested_yaml.items():
        expanded = schema
        if '.' in key:
            if key.strip()[-1] == '.':
                raise Exception('Malformed name: {}'.format(key))
            split_key = key.split('.')
            key = split_key[0]
            expanded = gen_fields_from_dots(split_key, schema)[key]
        elif 'fields' in schema:
            expanded = {
                'name': key,
                'description': schema['description'],
                'fields': expand_dots(schema['fields'])
            }

        merged[key] = merge(merged.get(key, {}), expanded)
    return merged


def gather_fields(key, schema):
    if 'fields' in schema:
        fields = []
        ret = {
            'name': key,
            # don't include type: group
            'description': schema['description'] if 'description' in schema else 'TODO',
            'fields': fields,
        }
        for name, obj in schema['fields'].items():
            fields.append(gather_fields(name, obj))
        return ret
    else:
        no_fields = {
            'name': key,
            'type': schema['type'],
            'description': schema['description'] if 'description' in schema else 'TODO',
        }
        if 'example' in schema:
            no_fields['example'] = schema['example']
        return no_fields


def get_schema_desc(path, name):
    with open(path, 'r') as f:
        ecs_schema = yaml.safe_load(f)

    for schema in ecs_schema:
        if schema['name'] == name:
            return schema['description'].rstrip()


def load_schema_from_dir(path, callback=None):
    schema_to_path = {}
    for f in os.listdir(path):
        file_no_ext = os.path.splitext(f)[0]
        file_full_path = os.path.join(path, f)
        # don't let the custom schema names override the ecs ones
        if os.path.isfile(file_full_path):
            # allows us to remove 'custom'
            if callback:
                file_no_ext = callback(file_no_ext)
            schema_to_path[file_no_ext] = file_full_path
    return schema_to_path


def load_schema_to_path(ecs_path, custom_schema_path):
    ecs_schema_path = os.path.join(ecs_path, 'schemas')
    ecs_schema = load_schema_from_dir(ecs_schema_path)

    def remove_custom(custom_name):
        if custom_name.startswith('custom_'):
            return custom_name.replace('custom_', '')
    custom_schema = load_schema_from_dir(custom_schema_path, remove_custom)

    for name, path in custom_schema.items():
        if name not in ecs_schema:
            ecs_schema[name] = path
    return ecs_schema


def recurse_fields(fields, ecs_schema):
    for f in fields:
        name = f['name']
        desc = f['description']
        if desc.lower() == 'todo' and name in ecs_schema:
            f['description'] = get_schema_desc(ecs_schema[name], name)
        if 'fields' in f:
            recurse_fields(f['fields'], ecs_schema)


def enrich_top_level_fields(event, ecs_path, custom_path):
    schema_to_path = load_schema_to_path(ecs_path, custom_path)
    recurse_fields(event['fields'], schema_to_path)


def create_event_example(subset, out, ecs_path, custom_path, out_schema_dir):
    subset_basename = os.path.basename(subset)
    subset_no_ext = os.path.splitext(subset_basename)[0]
    abs_out = os.path.abspath(out)
    abs_out_schema_dir = os.path.abspath(out_schema_dir)
    nested_ecs = os.path.join(abs_out, subset_no_ext, GEN_ECS)
    example = os.path.join(abs_out, subset_no_ext, subset_basename)

    with open(nested_ecs, 'r') as f:
        nested_yaml = yaml.safe_load(f)

    fields = []
    event = {
        # remove the extension
        'title': os.path.splitext(subset_basename)[0],
        'fields': fields
    }

    merged = expand_dots(nested_yaml)

    for key, obj in merged.items():
        if key == 'base':
            base = gather_fields(key, obj)
            fields.extend(base['fields'])
        else:
            fields.append(gather_fields(key, obj))

    enrich_top_level_fields(event, ecs_path, custom_path)

    with open(example, 'w') as out_file:
        stream = yaml.dump(event, default_flow_style=False, sort_keys=False)
        rep_stream = re.sub(r'\n( *)- name', r'\n\n\1- name', stream)
        out_file.write(rep_stream)

    print('Copy generated example file [{}] to {}'.format(subset_basename, abs_out_schema_dir))
    shutil.copy(example, abs_out_schema_dir)


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
    args.out_schema_dir = args.out_schema_dir or args.out
    print('out_schema_dir: {}'.format(args.out_schema_dir))

    subset_files = get_glob_files(args.subset)
    print('Found subset files: {}'.format(subset_files))

    for s in subset_files:
        generate_subset(args.ecs, args.custom_schema, s, args.out)
        create_event_example(s, args.out, args.ecs, args.custom_schema, args.out_schema_dir)


if __name__ == '__main__':
    main()
