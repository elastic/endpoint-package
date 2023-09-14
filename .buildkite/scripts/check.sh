#!/bin/bash

set -euo pipefail

echo "--- Install requirement"
set -x
echo "Install Go"
GO_INSTALLER=go1.21.1.linux-amd64.tar.gz
curl -O https://go.dev/dl/$GO_INSTALLER
mkdir ~/.local/
tar xzf $GO_INSTALLER -C $HOME/.local
export PATH=$HOME/.local/go/bin:$PATH
set +x

echo "Install elastic-package"
make elastic-package


echo "--- Retrieving stack version"
# Use STACK_VERSION if defined, else use the output of .buildkite/scripts/find_oldest_supported_version.py
_STACK_VERSION=${STACK_VERSION:-$(python3 .buildkite/scripts/find_oldest_supported_version.py)}
echo "Using stack version $_STACK_VERSION"

echo "--- Prepare stack"
echo "Update the Elastic stack"
./scripts/go-tools/bin/elastic-package stack update -v --version ${_STACK_VERSION}

echo "Boot up the Elastic stack"
./scripts/go-tools/bin/elastic-package stack up --services elasticsearch -d -v --version ${_STACK_VERSION}


echo "--- Static tests"
eval "$(./scripts/go-tools/bin/elastic-package stack shellinit)"
make static-test

echo "--- Pipeline tests"
eval "$(./scripts/go-tools/bin/elastic-package stack shellinit)"
make pipeline-test
