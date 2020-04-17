# Custom Subsets

This directory contains the definitions for generating ecs files (templates, docs, etc). The subset format allows us to
specify a subset of the ecs schema as well as custom definition to use when generating files.

For example, if you wanted to create a mapping file that only contained [host.os.platform](https://github.com/elastic/ecs/blob/master/schemas/os.yml#L16)
you would create a subset file as follows:

```yml
host:
  fields:
    os:
      fields:
        platform:
          fields: "*"
```

Or this shorthand (more info on that in this PR: <https://github.com/elastic/ecs/pull/805>)

```yml
host:
  fields:
    os:
      fields:
        platform: {}
```

## Generating the ECS files

To generate the ecs files, you will need to clone the ecs repo.

Once you have that cloned, you'll need to install the python package `requirements.txt` under the `scripts` directory.

The [scripts/generator.py](https://github.com/elastic/ecs/blob/master/scripts/generator.py) script is used to generate
the files. The scripts allows the flags:

- `--out` to point to the location to write the generated files

- `--include` to point to the `custom_schemas` [directory](../custom_schemas) or wherever your additional schema is located

- `--subset` in glob format to point to the subset files to use

### Generating templates

```bash
cd ecs
python scripts/generator.py --out ../gen --include ../endpoint-app-team/custom_schemas --subset ../endpoint-app-team/custom_subsets/elastic_endpoint/events/*
```

The generated files will be in `../gen`

### Generating the schema files

To generate the event schema files in [schemas](../schemas/v1) follow the instructions in the [event_schema_generator](../scripts/event_schema_generator/README.md)
