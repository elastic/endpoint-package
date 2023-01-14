
import os
import pprint
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

keeping = ["name", "fields"]
keeping_recursive = ["found_in"]

# here
HERE = os.path.abspath(os.path.dirname(__file__))

def recursive_filter(obj):
    keys = [x for x in obj.keys()]
    for key in keys:
        if key in keeping:
            if isinstance(obj[key], dict):
                recursive_filter(obj[key])
            elif isinstance(obj[key], list):
                for i in obj[key]:
                    recursive_filter(i)
            continue
        if key in keeping_recursive and isinstance(obj[key], dict):
            recursive_filter(obj[key])
            continue

        obj.pop(key)

# find all fields.yml
for root, dirs, files in os.walk(HERE):
    for f in files:
        if f == "fields.yml":
            with open(os.path.join(root, f)) as f:
                obj = yaml.load(f, Loader=Loader)

            for item in obj:
                recursive_filter(item)
            with open(os.path.join(root, "filtered.yml"), "w") as f:
                yaml.dump(obj, f, Dumper=Dumper, sort_keys=False)

