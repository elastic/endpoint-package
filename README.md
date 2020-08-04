# The Endpoint Package

The Endpoint package handles installing mapping templates, ILM policies, ingest pipelines, and other functionality
that should be done prior to the Endpoint streaming data to ES and using the Endpoint app in Kibana.

The Endpoint package is located [locally here](./package/endpoint) and [remotely here](https://github.com/elastic/package-storage/tree/master/packages/endpoint)

To update the endpoint package clone this repo and make changes as needed

## Tool Prerequisites

This section includes a list of tools that should be installed before making changes to the Endpoint's mapping.
The individual sections below will give more details about how each tool is used and setup.

- Install go 1.14 from here: <https://golang.org/dl/>

- Install `hub` tool via `brew install hub`

- Install python 3.7+

- Install pipenv via `brew install pipenv`

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

The created files will be in the directory `out`.

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
xpack.ingestManager.enabled: true
xpack.ingestManager.registryUrl: "http://127.0.0.1:8080"
xpack.ingestManager.fleet.enabled: true
```

The `xpack.ingestManager.registryUrl` flag instructs Kibana to look for the package registry at the specified URL.
By default Kibana uses the external package registry.

The Ingest Manager will now use your locally running package registry for retrieving a package. The Ingest Manager
within Kibana does some caching after it has downloaded a package, so if you are not seeing your changes you might
need to restart Kibana and Elasticsearch.

### PR the changes

After making and testing the necessary changes, PR them to this repo.

## Updating the package in the remote registry

There are three environments that provide different functionality for packages, snapshot, staging, and production.

Snapshot is used for testing packages. It is mainly accessed by running kibana from source off the `master` branch.

Staging is for packages that need a little more testing but are almost ready for production. The endpoint package's makefile
releases straight to staging because it expects changes to go through local testing already.

Production is used by deployments of the elastic stack.

To release a new endpoint package a PR will be opened against the package-storage repo <https://github.com/elastic/package-storage> with
the contents of the new endpoint package. A new version number directory should be created here: <https://github.com/elastic/package-storage/tree/staging/packages/endpoint> with the appropriate version number for this release. Once this PR is merged a docker image will be built containing
the new endpoint package. There is still a manual step of pushing the docker image to the staging environment.

TODO (this hasn't been implemented yet)
To do this, run `make release-staging`. This will open a draft PR to the `staging` branch for the package-storage repo.
The version of this package will intentionally be a dev version (i.e. `0.10.0-dev0`). That way if any issues are found they
can be fixed without needing to bump the major, minor, or patch again.

### Creating new docker images

Once the PR is merged to the `staging` branch CI will kick off a new build for that branch that will release a new docker image.
The images can be located here: <https://container-library.elastic.co/r/package-registry/distribution>

To create a new docker image for `snapshot` you might need to manually kick off a build for that branch which can be done here: <https://beats-ci.elastic.co/blue/organizations/jenkins/Beats%2Fpackage-storage/branches>

### Deploying a new registry with the package

Before deploying a new docker image you will need to be granted access. See [here](https://github.com/elastic/observability-dev/blob/master/docs/integrations/ingest-management/package-registry.md#getting-access) for more details.

To see all the available registries run:

`kubectl get deployment -n package-registry`

To deploy the package to the staging registry run: `kubectl rollout restart deployment package-registry-staging-vanilla -n package-registry`

Once all the pods restart you should be able to see the new package here: <https://epr-staging.elastic.co/search?package=endpoint>

To deploy a new docker image for `snapshot` and `production` use the commands below:

kubectl rollout restart deployment package-registry-snapshot-vanilla -n package-registry
kubectl rollout restart deployment package-registry-prod-vanilla -n package-registry

### Releasing package to production

TODO this isn't implemented yet
Once all the issues have been worked out while testing in `staging` the package is ready to be released in production.
First, run `make release-production` which will remove the prerelease portion of the version (i.e. `-dev0` etc) and open a
PR against the `production` branch.

After the PR to the `production` branch is merged and the CI publishes the docker image. Deploy the new registry by running:
`kubectl rollout restart deployment package-registry-prod-vanilla -n package-registry`
