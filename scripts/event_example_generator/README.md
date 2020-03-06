# Event Examples
This script takes the subset style files and outputs the full example of a given event.

# To run
You will need python 3.7

From the `endpoint-app-team/scripts/event_example_generator` directory

```bash
python main.py --out-schema-dir ../../schemas/v1 ../../../ecs ../../custom_schemas ../../custom_subsets/elastic_endpoint/events/*.yaml test
```