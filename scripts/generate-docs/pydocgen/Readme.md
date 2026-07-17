# Custom Documentation Generator

## Description

This module generates documentation for the custom endpoint fields defined in [custom_documentation](../../../custom_documentation/)

### Background

The fields defined in [custom_documentation](../../../custom_documentation/) do not have descriptions.  They are simply the possible fields
of an event, including all the custom fields Endpoint uses but are not mapped.

The fields defined in [package](../../../package/) are the fields that are mapped into Kibana.  These fields have descriptions and documentation.


### Implementation

This python module generates markdown for all of the fields in [custom_documentation](../../../custom_documentation/) by taking the following steps

1. Parses all of the mapped fields defined in [package](../../../package/), collecting descriptions, examples, and other metadata

2. Parses any override fields defined in [documentation_overrides.yaml](../../../custom_documentation/src/documentation_overrides.yaml)
   - overrides can be set for any field.  They can be set at the event level, the os level, or a default override that applies to all
    instances of that field.
   - See [documentation_overrides.yaml](../../../custom_documentation/src/documentation_overrides.yaml) for the format
   - If overrides are updated, the documentation must be regenerated

3. Puts all of that data into an sqlite database

4. Parses all of the endpoint fields defined in [custom_documentation](../../../custom_documentation/)

5. Iterates over the custom_documentation data, filling out descriptions and examples pulled from the database that was just created.

### Example Usage
`python -m pydocgen --output-dir /path/to/output`

#### Help statement
```
usage: __main__.py [-h] [--database DATABASE] [--no-cache] [--output-dir OUTPUT_DIR] [-v] [-l {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--csv CSV]

Create markdown documentation for the fields defined in custom_documentation

options:
  -h, --help            show this help message and exit
  --database DATABASE   path to the database
  --no-cache            do not use cached database if it exists, always regenerate the database
  --output-dir OUTPUT_DIR
                        output directory for markdown documentation
  -v, --verbose         Force maximum verbosity (DEBUG level + detailed output)
  -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}, --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set logging verbosity level
  --csv CSV             Path to CSV file for missing documentation fields (optional)

Example usage: python -m pydocgen --output-dir /path/to/output
```
