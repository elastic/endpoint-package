import argparse
import subprocess
import glob
import os
import yaml

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
    subset_out = os.path.join(os.path.abspath(out), os.path.basename(subset_file))
    print('Generating subset fields for: {}'.format(subset_file))
    ret = subprocess.run(['python', ECS_SCRIPT, '--include', os.path.abspath(custom_schema),
                          '--subset', os.path.abspath(subset_file),
                          '--out', subset_out], stdout=subprocess.PIPE, check=True,
                         cwd=ecs_path, universal_newlines=True)
    print('Generation output-----------------')
    for line in ret.stdout.splitlines():
        print(line,)
    print('Finished generating subset-----------------')


def gather_fields(key, schema):
    if 'fields' in schema:
        fields = []
        ret = {
            'name': key,
            'fields': fields,
            'description': schema['description'],
            'type': schema['type']
        }
        for name, obj in schema['fields'].items():
            fields.append(gather_fields(name, obj))
        return ret
    else:
        return {
            'name': key,
            'description': schema['description'],
            'type': schema['type'],
            'example': schema['example'] if 'example' in schema else ''
        }


def create_event_example(subset, out):
    subset_basename = os.path.basename(subset)
    abs_out = os.path.abspath(out)
    nested_ecs = os.path.join(abs_out, subset_basename, GEN_ECS)
    example = os.path.join(abs_out, subset_basename, subset_basename)

    with open(nested_ecs, 'r') as f:
        nested_yaml = yaml.safe_load(f)

    fields = []
    event = {
        # remove the extension
        'title': os.path.splitext(subset_basename)[0],
        'fields': fields
    }

    for key in nested_yaml:
        if key == 'base':
            base = gather_fields(key, nested_yaml[key])
            fields.extend(base['fields'])
        else:
            fields.append(gather_fields(key, nested_yaml[key]))

    with open(example, 'w') as out_file:
        yaml.dump(event, out_file, default_flow_style=False, sort_keys=False)


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
