import argparse
import subprocess
import glob
import os
import yaml
import re

ECS_SCRIPT = 'scripts/generator.py'
GEN_ECS = 'generated/ecs/ecs_nested.yml'


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('ecs', help='path to the root directory of the ecs project')
    parser.add_argument('custom_schema', help='path to custom schema directory')
    parser.add_argument('subset', nargs='+', help='one or more glob style directories of subset definitions')
    parser.add_argument('out', help='directory to store the generated files')
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


def create_event_example(subset, out):
    subset_basename = os.path.basename(subset)
    subset_no_ext = os.path.splitext(subset_basename)[0]
    abs_out = os.path.abspath(out)
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

    with open(example, 'w') as out_file:
        stream = yaml.dump(event, default_flow_style=False, sort_keys=False)
        rep_stream = re.sub(r'\n( *)- ', r'\n\n\1- ', stream)
        out_file.write(rep_stream)


def get_glob_files(paths):
    all_files = []
    for path in paths:
        all_files.extend(glob.glob(path))

    return all_files


def main():
    args = argument_parser()

    print('ecs: {}'.format(args.ecs))
    print('custom_schema: {}'.format(args.custom_schema))
    print('subset: {}'.format(args.subset))
    print('out: {}'.format(args.out))

    subset_files = get_glob_files(args.subset)
    print('Found subset files: {}'.format(subset_files))

    for s in subset_files:
        generate_subset(args.ecs, args.custom_schema, s, args.out)
        create_event_example(s, args.out)


if __name__ == '__main__':
    main()
