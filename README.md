# The Endpoint Package

test

The Endpoint package handles installing mapping templates, ILM policies, ingest pipelines, and other functionality
that should be done prior to the Endpoint streaming data to ES and using the Endpoint app in Kibana.

To update the endpoint package clone this repo and make changes as needed



## Contributing and Making Changes

### Tool Prerequisites

This section includes a list of tools that should be installed before making changes to the Endpoint's mapping.
The individual sections below will give more details about how each tool is used and setup.

- Install go 1.14 from here: <https://golang.org/dl/>

- Install [Python 3.6+](https://www.python.org/)



### Mapping changes

#### Updating the Endpoint Package Mapping

To update the endpoint package mapping take a look at the [Custom Schema](./custom_schemas/README.md) and
[Custom Subset](./custom_subsets/README.md) first to get an understanding of what makes up the mapping.

The essential steps are listed here:

- Edit/add custom schema files as needed to define any fields that don't exist in ECS core

- Update the subset files for the particular event that is being changed or create a new subset file

- If a new type of document is being added that doesn't fit in the existing ones (e.g. events),
  create a new directory in `custom_subsets/elastic_endpoint` to contain the subset files

- Generate the mapping

#### Generating the mapping

Run `make` (to speed things up try running `make -j8`)

The files will be built into the directory `out`, with the important reference files copied to `generated`, and `schemas`, and the final package file in `package/endpoint/data_stream/*/fields/fields.yml`

If you believe `make` is not picking up your changes, you can force a rebuilt with the `-B` option:

```sh
make -B -j12
```

#### Note about the ECS Version

The generated files are dependent on the github version of ECS used. To use a more recent version
of ECS to pick up new definition chance the `ECS_GIT_REF` in the **Makefile**. You can also
make a temporary change command line `make ECS_GIT_REF=v1.6.0`. But be sure to commit this to the
**Makefile** when you are done and satisfied with your change.

#### Testing Changes

Once you've generated the new mappings, you'll want to test the changes. To test changes to the Endpoint package you will need to point your Kibana at a locally running package registry.
More details about the package registry are [here](https://github.com/elastic/package-registry/blob/master/README.md#running)

Use the `make run-registry` command to quickly run a package registry locally once you have go installed.

Add the follow flags to your `kibana.dev.yaml` file

```yaml
xpack.fleet.registryUrl: "http://127.0.0.1:8080"
```

The `xpack.fleet.registryUrl` flag instructs Kibana to look for the package registry at the specified URL.
By default Kibana uses the external package registry.

The Ingest Manager will now use your locally running package registry for retrieving a package. The Ingest Manager
within Kibana does some caching after it has downloaded a package, so if you are not seeing your changes you might
need to restart Kibana and Elasticsearch.

If you want to check you are using the correct Ingest manager go to Management -> Integrations in Kibana and search for Elastic Defend. It is likely that you are testing a pre-release version. In order to test properly, enable the Display beta integrations switch on this page. Afterwards, you will see a beta version of Elastic Defend in the UI. Observe the version number. You should see the -dev or -next sufix in the version. Add this version of Elastic Defend to your Agent Policy to install the package and test it.

If you don't see your version in the Integration you want to make sure the Ingest Manager is running correctly you can try a request to test it:

```bash
curl "http://localhost:8080/search?package=endpoint"
```

If you see a JSON response, the Ingest Manager is running and it is probably a problem in your Kibana configuration. If you don't get a response you should check the running Ingest Manager process you probably started with docker.

Note, since you are likely testing a pre-release version of the package, to ensure that the dev package that you're testing is in your locally running registry, add the `prerelease` flag to the query param.

```bash
curl "http://localhost:8080/search?package=endpoint&prerelease=true"
```


#### PR the changes

After making and testing the necessary changes, PR them to this repo.


#### Exceptionable

In the Kibana UI, if you want to add a field to appear as "exceptionable", appearing in the Exceptions drop-down autofill menu, that change is made in Kibana. Here is an [example PR](https://github.com/elastic/kibana/pull/129401) of a similar change to follow.



## Release Process

Github actions are set up to publish the Endpoint package automatically when new changes merge. All merges and changes to the `main` branch get published as "prerelease" versions, but are otherwise available over the internet. To publish a "production" or "stable" release, we must simply publish a change to the `main` branch with a typical semver (i.e. `x.y.z`) in `package/endpoint/manifest.yml`.

To keep things tidy, satisfy the linting deities, and make it easier to backport in the future, there is a recommended flow to accomplish a stable release. At a high level the steps are:

1. [Prep release](#prep-release)
2. [Merge](#merge)
3. [Tag](#tag)
4. [Release Tracking branch](#release-tracking-branch)
5. [Setup for next dev cycle](#setup-for-next-dev-cycle)


### Prep Release

1. Create a new working branch for the release work
2. Gather up the list of PRs that have been merged since last release
  - e.g. https://github.com/elastic/endpoint-package/compare/v8.5.0...main
3. Update `package/endpoint/changelog.yml` with summaries of each PR
  - you may skip entries that are specific to repository maintenance and administration. The changelog should only reflect changes _to the package contents_. Schemas, changes that would be visible to the shipped integration, etc.
  - `elastic-package` tool can be used to automate additions:
    + `./scripts/go-tools/bin/elastic-package changelog add --description <PR-title> --link <github-link> --type enhancement --version 8.6.0`
  - the changelog file can be checked and linted with the `elastic-package` tool
4. Set the release version in `package/endpoint/manifest.yml`. This will likely mean stripping of any `-dev.N` or `-next` suffixes on the `version` field
5. Commit, push & PR the working branch to the main repo branch
  - Example pull request you should have at this point: https://github.com/elastic/endpoint-package/pull/301
  
### Merge

Get approvals on your release PR, and merge


### Tag


1. After approval & merge, pull the upstream merge commit into your local
1. Create a release tag (e.g. `v8.6.0`) pointing to this merge commit that was just made, and `git push --tags` to the upstream repo

### Release Tracking Branch

1. Create a release tracking branch. i.e. if you just released 8.6.0, create a branch `8.6` to track the `8.6.x` minor series
1. push the branch reference
1. Create a new working branch on top of this release tracking branch
1. Change `package/endpoint/manifest.yml` to be the development cycle for the next release in that series.
  - e.g. if `8.6.0` was just released, the version should now be `8.6.1-dev.0`
1. Commit this to your working branch. Push & PR to the release tracking branch (e.g. `8.6`)
  - example commit for this: https://github.com/elastic/endpoint-package/commit/79216929cbcf05d39e6bba5a85cf4062bc7682b8



### Setup for Next Dev Cycle

1. Checkout the `main` branch
2. Create a new working branch
3. Change `package/endpoint/manifest.yml` to be the development series for the next release. (e.g. if `8.6.0` was just released, version should now be `8.7.0-dev.0`).
4. Change `conditions.kibana.version` in that same file to match the new stack version (e.g. change from `^8.6.0` to `^8.7.0`)
5. Commit, push, PR to the main branch
  - example PR for these changes: https://github.com/elastic/endpoint-package/pull/302
  


To do: coordinate and update the bundled package version in fleet



