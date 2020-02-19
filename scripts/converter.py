import json
import sys

def rekey_alert(old_alert, new_alert, mapping):

    for key, val in mapping.items():
        if isinstance(val, dict):
            field = old_alert.get(key, None)
            if field is None:
                continue
            if isinstance(field, list):
                # To maintain the internal relationship within list items we rekey each item within a list independently
                # Crash here if we can't find ~list_prefix since the mapping is malformed, add a descriptive error message later maybe
                new_list_prefix = val["~list_prefix"].split('.')
                new_location = new_alert
                for list_key in new_list_prefix[:-1]:
                    new_location = new_alert.setdefault(list_key, {})
                new_location[new_list_prefix[-1]] = []
                for item in field:
                    new_item = {}
                    rekey_alert(item, new_item, val["~entry_mapping"])
                    new_location[new_list_prefix[-1]].append(new_item)
            else:
                rekey_alert(field, new_alert, val)
        else:
            new_keys = val.split('.')
            new_location = new_alert
            if key in old_alert:
                for new_key in new_keys[:-1]:
                    new_location = new_location.setdefault(new_key, {})
                new_location[new_keys[-1]] = old_alert[key]
                old_alert.pop(key)


def main(argv):
    source_alert = json.load(open(argv[0]))
    mapping = json.load(open(argv[1]))
    new_alert = {}
    rekey_alert(source_alert, new_alert, mapping)
    with open('leftovers.json', 'w') as out:
        json.dump(source_alert, out, indent=2)
    with open('rekeyed.json', 'w') as out:
        json.dump(new_alert, out, indent=2)


if __name__ == "__main__":
    main(sys.argv[1:])
