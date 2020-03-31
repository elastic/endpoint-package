# Endpoint-app-team
Internal issue and project tracking repo for Endpoint App team


# Running Kibana with Endpoint App Enabled from Kibana.

From https://github.com/elastic/kibana/blob/master/CONTRIBUTING.md#setting-up-your-development-environment 

### Setting Up Your Development Environment

Fork, then clone the `kibana` repo and change directory into it

```bash
git clone https://github.com/[YOUR_USERNAME]/kibana.git kibana
cd kibana
```

Install the version of Node.js listed in the `.node-version` file. This can be automated with tools such as [nvm](https://github.com/creationix/nvm), [nvm-windows](https://github.com/coreybutler/nvm-windows) or [avn](https://github.com/wbyoung/avn). As we also include a `.nvmrc` file you can switch to the correct version when using nvm by running:

```bash
nvm use
```

Install the latest version of [yarn](https://yarnpkg.com).

Bootstrap Kibana and install all the dependencies

```bash
yarn kbn bootstrap
```

> Node.js native modules could be in use and node-gyp is the tool used to build them. There are tools you need to install per platform and python versions you need to be using. Please see https://github.com/nodejs/node-gyp#installation and follow the guide according your platform.

(You can also run `yarn kbn` to see the other available commands. For more info about this tool, see https://github.com/elastic/kibana/tree/master/packages/kbn-pm.)

When switching branches which use different versions of npm packages you may need to run;
```bash
yarn kbn clean
```

If you have failures during `yarn kbn bootstrap` you may have some corrupted packages in your yarn cache which you can clean with;
```bash
yarn cache clean
```

##  Running Kibana and  Elasticsearch
Once you have everything setup have  two tabs (one for Kibana, and one for Elasticsearch)

One tab:

`$ npx yarn es snapshot --license trial -E discovery.type="single-node" -E network.host="0.0.0.0"`

Another Tab:

`$ yarn start --verbose --host=0.0.0.0 --csp.strict=false --xpack.endpoint.enabled=true`

Elasticsearch will run on http://127.0.0.1:9200 and Kibana on http://127.0.0.1:5601

##  Generating sample endpoint metadata documents, alerts, and associated resolver events
In a new CLI tab, change directory to kibana/x-pack/plugins/endpoint, then run:

`$ yarn test:generate --auth elastic:changeme`

The default settings generate a single endpoint metadata document, a single alert, and a few associated events for the resolver tree.

## Clearing out ES data (starting fresh)
Stop kibana and ES then run
`$ rm -r .es`
Then start kibana / Elasticsearch again with a fresh/clean environment. 

