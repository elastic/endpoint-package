# Event Schema

This script takes the subset style files and outputs the full schema of a given event.

## To run

### Setup

Before generating the schema files you'll need to clone the [ecs repo](https://github.com/elastic/ecs) (master branch).
Once you have that cloned, you'll need to install the python package `requirements.txt` under the `scripts` directory
[here](https://github.com/elastic/ecs/blob/master/scripts/requirements.txt).

This project relies on dictionaries being ordered
so you'll need python 3.6 or greater. It's probably easiest to `brew install python` and use
`python3`. If you run into issues installing, it might be because of macOS Catalina, try `brew reinstall python`

### Usage

```bash
usage: main.py [-h] [--out-schema-dir directory where example file will be copied]
               <path to ecs repo> <path to custom_schema dir> subset [subset ...] <path to output directory used by ecs to generate temporary files>
```

From the `endpoint-app-team/scripts/event_schema_generator` directory

```bash
python main.py --out-schema-dir ../../schemas/v1 ../../../ecs ../../custom_schemas ../../custom_subsets/elastic_endpoint/events/*.yaml test
```

With virtualenv:

```bash
. venv/bin/activate
python main.py --out-schema-dir ../../schemas/v1 ../../../ecs ../../custom_schemas ../../custom_subsets/elastic_endpoint/events/*.yaml test
```
