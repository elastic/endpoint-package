#!/bin/bash
#

set -euo pipefail

echo "--- Install python3 virtualenv"
apt update -y && apt install -y python3.11-venv

echo "--- Build"
make
