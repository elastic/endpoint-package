---
name: Schema Change
about: Adds/Removes/changes any schema fields
labels: 'schema, Team:Onboarding and Lifecycle Mgt'
---

## Change Summary

<!-- please describe the intended use for the field changes -->

#### Sample values

<!--  Please provide sample values that will go into these field changes. 
    
    This ticket is a good reference: https://github.com/elastic/endpoint-dev/issues/9533
-->

Sample document:

```json


```


## Release Target

<!-- What is intended Kibana release this is expected to ship with -->


## Q/A

- [ ] I ran `make` after making the schema changes, and committed any generated files (in `schema/`, `generated/`)
- [ ] Does this field need to be "exceptionable"? (no longer specified in this package, this is now tracked in Kibana)
- [ ] If this is a `metadata` change, I also updated both transform destination schemas to match