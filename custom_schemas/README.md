# Custom Schema

This directory stores definitions of fields not present in the core ECS schema. These fields are used in the
Endpoint Package to define the mapping for documents stored in Elasticsearch.

These schema files are the same format as those in the ECS repository and can either supplement a top level field
(e.g. http, os, etc) or add a definition for a completely new field (e.g. endpoint).

## Supplementing top level ECS fields

An example of supplementing a top level field is the [custom_os.yml](custom_os.yml) file:

```yml
---
- name: os
  title: Custom OS
  group: 2
  short: TODO
  description: >
    TODO
  type: group
  fields:
    - name: variant
      level: custom
      type: keyword
      description: >
        A string value or phrase that further aid to classify or qualify the operating system (OS).
        For example the distribution for a Linux OS will be entered in this field.
      example: Ubuntu
```

The top level field `os` exists in ECS [here](https://github.com/elastic/ecs/blob/master/schemas/os.yml)
but the `variant` field is not defined within ECS. This allows the metadata
mapping to include a definition for the `variant` field without having to change ECS.

## Creating new top level field

An example of creating a new top level field is the [custom_endpoint.yml](custom_endpoint.yml) file:

```yml
---
- name: endpoint
  title: Endpoint
  group: 2
  short: Fields describing the state of the Elastic Endpoint when an event occurs.
  description: >
    Fields describing the state of the Elastic Endpoint when an event occurs.
  type: group
  fields:
    - name: policy
      level: custom
      type: object
      description: The policy fields are used to hold information about applied policy.

    - name: policy.id
      level: custom
      type: keyword
      description: >
        ID of the policy that was active when the event was created.
      example: c2a9093e-e289-4c0a-aa44-8c32a414fa7a
```

## Making changes

The required variables for adding new fields are:

- `name` - the name of the field that will show up in the mapping

- `level` - set to `custom`

- `type` - the Elasticsearch field type (e.g. `keyword`, `long`, etc)

- `description` - a text description of what the field is used for

Optional (but a good idea) variables:

- `example` - an example value for the field

- `allowed_values` - a list of allowed values for the field (example here: <https://github.com/elastic/ecs/blob/master/schemas/event.yml#L132>)

When adding a new file name it `custom_<top level field name>`.

### Defining a description on an object field

In the `endpoint` example it is option to define the parent object for a child field. When creating a new field
`endpoint.a_field.some_field`, you don't have to create a definition for `a_field` similar to what is above. You could
only have the following:

```yml
---
- name: endpoint
  title: Endpoint
  group: 2
  short: Fields describing the state of the Elastic Endpoint when an event occurs.
  description: >
    Fields describing the state of the Elastic Endpoint when an event occurs.
  type: group
  fields:
    - name: a_field.some_field
      level: custom
      type: keyword
      description: >
        ID of the policy that was active when the event was created.
      example: c2a9093e-e289-4c0a-aa44-8c32a414fa7a
```

The advantage of defining the parent field:

```yml
- name: a_field
    level: custom
    type: object
    description: The policy fields are used to hold information about applied policy.
```

is that it will produce a `description` when generating the schema files in [schemas](../schemas/v1). If you don't
specify the parent field, the description for `a_field` will default to `TODO`.

For example, the `policy` description is used in the [metadata.yaml](../schemas/v1/metadata.yaml)

```yml
- name: endpoint
  description: Fields describing the state of the Elastic Endpoint when an event
    occurs.
  fields:
    - name: policy
      description: The policy fields are used to hold information about applied
        policy.
      fields:
        - name: id
          type: keyword
          description: ID of the policy that was active when the event was created.
          example: c2a9093e-e289-4c0a-aa44-8c32a414fa7a
```
