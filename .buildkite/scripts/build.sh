#!/bin/bash
#

set -euo pipefail

echo "--- Install python3 virtualenv"
apt update -y && apt install -y python3.11-venv


echo "--- Build"
make


echo "--- Check Git Diff"
echo "update git index"
git update-index -q --really-refresh

echo "check for uncommitted build artifacts"
git diff-index --exit-code HEAD --
