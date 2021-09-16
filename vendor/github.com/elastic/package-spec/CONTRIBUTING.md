# Contributing

## Change Proposals

Any changes to Elastic Stack products or Elastic Packages that require changes to the Elastic Package Specification 
must be discussed first and then safely implemented across impacted products. At a high level, this process looks
something like this:

1. Propose your change via a [new Change Proposal issue](https://github.com/elastic/package-spec/issues/new/choose) 
   in the `package-spec` repository (i.e. this repository). This gives us an opportunity to understand which parts of the 
   Elastic Stack might be impacted by this change and pull in relevant experts to get their opinions. The initial proposal 
   should cover these areas:
   - What problem the proposal is solving. This provides context and could help shape the solution.
   - Where the solution will need to be implemented, i.e. which parts, if any, of the Elastic Stack will be impacted. It's 
     okay if the initial proposal doesn't get this 100% right; the discussion in the proposal issue should provide clarity.
     Feel free to tag relevant experts to get their opinions.

2. Discussion ensues and eventually we hope to reach some consensus.

3. Once there's consensus on the proposal issue, modify the issue description to include an **ordered** checklist of 
   tasks that need to be resolved to make the change happen in a safe way.  For example, maybe Kibana needs to implement 
   support for a new property in the Package Specification first, then only when that support is implemented, the Package
   Specification can itself be modified, which would then allow packages to define this property and have these packages 
   still be valid. At this point the proposal issue serves as a meta issue for the safe implementation of the change.

4. File issues in each of the repositories corresponding to the checklist items and update the checklist with links to 
   these issues.

5. No single PR may close the proposal issue. But as these PRs get resolved, the corresponding checklist item should be 
   checked off. The proposal issue is closed when all items are checked off.


## Folder Item spec

### Using predefined placeholders in filename patterns

There are predefined placeholders that can be used in filename patterns. Standard patterns are simple regular expressions
like `[a-z0-9]+\.json`. In some cases it might be useful to introduce a harder requirement (binding), e.g. a filename should
be prefixed with a package name (`{PACKAGE_NAME}-.+\.json`).

Currently, the following placeholders are available:

* `{PACKAGE_NAME}` - name of the package

## Folder Item schema

### Defining property format

The JSON Schema defines the basic structure of a JSON document (e.g. package manifests, ingest pipelines, etc.).
In some cases this might be insufficient as there are properties that require strict validation (not just type
consistency), e.g. format validation:

```yaml
src:
  description: Relative path to the screenshot's image file.
  type: string
  format: relative-path
  examples:
  - "/img/apache_httpd_server_status.png"
```

Currently, the following custom formats are available:

* `relative-path`: Relative path to the package root directory. The format checker verifies if the path is correct and
  the file exists.
* `data-stream-name`: Name of a data stream. The format checker verifies if the data stream exists.