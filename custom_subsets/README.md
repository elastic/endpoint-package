# Custom Subsets

This directory contains the definitions for generating ecs files (templates, docs, etc). The subset format allows us to
specify a subset of the ecs schema as well as custom definition to use when generating files.

## Generating the ECS files

To generate the ecs files, you will need to clone the ecs repo. As of 3/19/20 there are some fixes that haven't been
merged into the mainline repo so it's recommended to use this <https://github.com/jonathan-buttner/ecs/tree/sub-set-fixes> branch
for the time being.

Once you have that cloned, you'll need to install the python package `requirements.txt` under the `scripts` directory.

### Generating templates and docs

```bash
cd ecs
python scripts/generator.py --out ../gen --include ../endpoint-app-team/custom_schemas --subset ../endpoint-app-team/custom_subsets/elastic_endpoint/events/* ../endpoint-app-team/custom_subsets/*.yml
```

The generated files will be in `../gen`

### Generating the schema files

To generate the example schema files in [schemas](../schemas) follow the instructions in the [event_schema_generator](../scripts/event_schema_generator/README.md)
