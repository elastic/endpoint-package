# Generate docs

The script allows for regenerating README docs based on the existing package content and the docs templates stored in
[doc_templates](../../doc_templates).

Template for README.md file supports following template functions:

`{{fields "access"}}` - render a table with exported fields for the dataset `access`

`{{event "access"}}` - render a sample event for the dataset `access`. The dataset event must be present in the
`{packageName}/dataset/{datasetName}/sample_event.json` file.

## Getting started

Navigate to the root directory and execute the following command:

```bash
go run ./scripts/generate-docs
```

This tool is run as part of the make build process so it will be invoked when `make` is run.
