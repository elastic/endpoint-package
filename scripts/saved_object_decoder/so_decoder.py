import json
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', action='store',
                        help='saved objects file to parse')
    parser.add_argument('out', action='store',
                        help='directory to write output files')
    return parser.parse_args()


def decode_json(saved_obj, to_decode):
    for key, val in to_decode.items():
        if key not in saved_obj:
            continue
        for field in val:
            if isinstance(field, dict):
                decode_json(saved_obj[key], field)
            elif isinstance(field, str) and field in saved_obj[key]:
                saved_obj[key][field] = json.loads(saved_obj[key][field])

    return saved_obj


def parse_json_line(output, data):
    data_id = data['id']
    data_type = data['type']
    if data_type == 'index-pattern':
        data_type = 'index_pattern'
    
    attributes_to_decode = {
        "attributes": [
            "uiStateJSON",
            "visState",
            "optionsJSON",
            "panelsJSON",
            "mapStateJSON",
            "layerListJSON",
            {"kibanaSavedObjectMeta": ["searchSourceJSON"]},
        ]
    }

    output[data_type][data_id] = {
        'title': data['attributes']['title'],
        'data': data
    }


def main():
    args = parse_args()
    output = {}
    dirs_to_make = ['index_pattern', 'visualization', 'dashboard', 'search', 'map']
    for name in dirs_to_make:
        output.setdefault(name, {})

    with open(args.file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            data = json.loads(line)
            if 'exportedCount' in data:
                continue
            parse_json_line(output, data)

    for vis_type, ids in output.items():
        if len(ids) != 0:
            os.makedirs(os.path.join(args.out, vis_type), exist_ok=True)
        for vis_id, vis_info in ids.items():
            name = vis_id
            with open(os.path.join(args.out, vis_type, '{}.json'.format(name)), 'w') as write_file:
                json.dump(vis_info['data'], write_file, indent=4)


if __name__ == '__main__':
    main()
