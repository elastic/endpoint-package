# Event Examples

This script takes the subset style files and outputs the full example of a given event.

## To run

### Setup

Before generating the example files you'll need to clone the ecs repo. As of 3/19/20 there are some fixes that haven't been
merged into the mainline repo so it's recommended to use this <https://github.com/jonathan-buttner/ecs/tree/sub-set-fixes> branch
for the time being.

Once you have that cloned, you'll need to install the python package `requirements.txt` under the `scripts` directory.

You'll also need python version 3.6 or greater

### Usage

```bash
usage: main.py [-h] [--out-schema-dir directory where example file will be copied]
               <path to ecs repo> <path to custom_schema dir> subset [subset ...] <path to output directory used by ecs to generate temporary files>
```

From the `endpoint-app-team/scripts/event_example_generator` directory

```bash
python main.py --out-schema-dir ../../schemas/v1 ../../../ecs ../../custom_schemas ../../custom_subsets/elastic_endpoint/events/*.yaml test
```
