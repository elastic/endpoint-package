# The Endpoint Package

The Endpoint package handles installing mapping templates, ILM policies, ingest pipelines, and other functionality
that should be done prior to the Endpoint streaming data to ES and using the Endpoint app in Kibana.

The Endpoint package is located [locally here](./package/endpoint) and [remotely here](https://github.com/elastic/package-storage/tree/production/packages/endpoint)

To update the endpoint package clone this repo and make changes as needed

## Tool Prerequisites

This section includes a list of tools that should be installed before making changes to the Endpoint's mapping.
The individual sections below will give more details about how each tool is used and setup.

- Install go 1.14 from here: <https://golang.org/dl/>

- Install [Python 3.6+](https://www.python.org/)

- Install [hub](https://github.com/github/hub) tool:
  - mac: `brew install hub`
  - debian-based: `sudo apt install hub`

NOTE: If you are using a higher version than python3 the make command may fail. You'll have to edit the Makefile and replace `3.7` with your python version.

## Updating the Endpoint Package Mapping

To update the endpoint package mapping take a look at the [Custom Schema](./custom_schemas/README.md) and
[Custom Subset](./custom_subsets/README.md) first to get an understanding of what makes up the mapping.

The essential steps are listed here:

- Edit/add custom schema files as needed to define any fields that don't exist in ECS core

- Update the subset files for the particular event that is being changed or create a new subset file

- If a new type of document is being added that doesn't fit in the existing ones (e.g. events),
  create a new directory in `custom_subsets/elastic_endpoint` to contain the subset files

- Generate the mapping

### Generating the mapping

Run `make` (to speed things up try running `make -j8`)

The files will be built into the directory `out`, with the important reference files copied to `generated`, and `schemas`, and the final package file in `package/endpoint/data_stream/*/fields/fields.yml`

If you believe `make` is not picking up your changes, you can force a rebuilt with the `-B` option:

```sh
make -B -j12
```

### Note about the ECS Version

The generated files are dependent on the github version of ECS used. To use a more recent version
of ECS to pick up new definition chance the `ECS_GIT_REF` in the **Makefile**. You can also
make a temporary change command line `make ECS_GIT_REF=v1.6.0`. But be sure to commit this to the
**Makefile** when you are done and satisfied with your change.

### Testing Changes

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

### PR the changes

After making and testing the necessary changes, PR them to this repo.


### Exceptionable

In the Kibana UI, if you want to add a field to appear as "exceptionable", appearing in the Exceptions drop-down autofill menu, that change is made in Kibana. Here is an [example PR](https://github.com/elastic/kibana/pull/129401) of a similar change to follow.


## Updating the package in the remote registry

There are three environments that provide different functionality for packages: snapshot, staging, and production.

Snapshot is used for testing packages. It is mainly used by running kibana from source off the `main` branch. The endpoint package's
release manager script releases to `snapshot`.

Staging is for packages that need a little more testing but are almost ready for production.

Production is used by official deployments of the elastic stack.

To release a new endpoint package a PR will be opened against the package-storage repo <https://github.com/elastic/package-storage> with
the contents of the new endpoint package. A new version number directory should be created here: <https://github.com/elastic/package-storage/tree/snapshot/packages/endpoint> with the appropriate version number for this release. Once this PR is merged a docker image will be built containing
the new endpoint package. There is still a manual step of pushing the docker image to the snapshot environment.

### Release a new package to v2 package storage

These steps will walk you through how to push a new package to package storage v2.  Package storage v2 will take new packages and publish them directly to production and make them available based on the version number.  If you push a new package with an incremented version, i.e. `v8.6.0 -> v8.7.0`, the new package will be pushed.  If you push a package with a `dev` or `next` postfix in it, such as `v8.7.0-next`, it will push to package storage, but it will not be available for use by production servers.

1. Create a working branch to make changes in
2. Compile the PRs that have been merged since last release
    - e.g. https://github.com/elastic/endpoint-package/compare/v8.6.0...main
3. Update `package/endpoint/changelog.yml` with summaries of each PR.
    - you can skip things that are specific to the repository maintenance and administration. The changelog is only about changes _to the package contents_. Schemas, changes that would be visible to the shipped integration, etc.
    - `elastic-package` can be used to automate additions:
      - `./scripts/go-tools/bin/elastic-package changelog add --description <PR-title> --link <github-link> --type enhancement --version 8.6.0`
  - the file can be checked and linted with the elastic-package tool
4. Set version in `package/endpoint/manifest.yml`. This will likely mean stripping off any `-dev.N` postfixes on the `version` field. That's all
5. Commit, push & PR your work to the main repo branch
6. Example pull request you should have at this point: https://github.com/elastic/endpoint-package/pull/312/files
7. After team approval & merge, pull the upstream change into your local
8. create a tag (e.g. `v8.6.0`) pointing to the merge commit that was just made, and `git push --tags` to the upstream repo
  - do not skip, some external teams use our release tags as automation points
9. Create a release-track branch. I.e. if you just released 8.6.0, create a branch `8.6` to track the 8.6.x minor series.
10. Push the branch reference
11. Create a new working branch
  - Change `package/endpoint/manifest.yml` version to be `8.6.1-dev.0`, to reflect the development series for what could become the 8.6.1 release in the future. PR these changes to the `8.6` branch.
  - example commit for this: https://github.com/elastic/endpoint-package/commit/79216929cbcf05d39e6bba5a85cf4062bc7682b8
12. checkout the main repo branch once again. Create a new working branch. 
  - change `package/endpoint/manifest.yml` to be the development series for the next release (e.g. if 8.6.0 was just released, version should now be `8.7.0-dev.0`).
  - change `conditions.kibana.version` in that same file to match (e.g. change from `^8.6.0` to `^8.7.0`).
  - commit, push, PR to main branch
  - example PR for these changes: https://github.com/elastic/endpoint-package/pull/302

After following the above steps, your package should be pushed to package storage.  You can check for it by visiting `https://epr.elastic.co/search?package=endpoint`  verifying that the response has the version you expect.