#!/bin/bash
#
# The script upload package for signing and publishing.
#
# Usage:
#   upload.sh sign|publish <package_dir>
#

set -euo pipefail

CMD="${1:-unknown}"
PACKAGE_DIR="${2:-build/packages}"


#
# Check if a given zip file is already published
#
is_published() {
    local _STATUS
    _STATUS="$(curl --head --output /dev/null --write-out "%{http_code}" "https://package-storage.elastic.co/artifacts/packages/$1")"
    
    if [ "$_STATUS" == "200" ]; then
        return 0
    fi

    return 1
}


#
# Upload package file for signing
#
upload_for_sign() {

    local _PKG_DIR
    _PKG_DIR="${1}"

    echo "--- Uploading unpublished artifacts from $_PKG_DIR for signing"

    buildkite-agent artifact download "build/packages/*.zip" "$_PKG_DIR"

    mkdir -p artifacts-to-sign
    find "$_PKG_DIR" -name "*.zip" | sort | while read -r _PKG; do
        
        echo "Checking if $_PKG is already published."
        if is_published "$_PKG"; then
            echo "$_PKG is already published. Skipping."
            continue
        fi

        mv "$_PKG" artifacts-to-sign/

    done

}


#
# Upload package and signature file for publish
#
upload_for_publish() {

    local _PKG_DIR
    _PKG_DIR="${1}"

    echo "--- Performing buildkite-agent step get"
    buildkite-agent step get --step package_sign --format json

    echo "--- Uploading unpublished artifacts from $_PKG_DIR for publishing"
    buildkite-agent artifact download "build/packages/*.asc" "$_PKG_DIR"

    find "$_PKG_DIR" -name "*.asc" | sort | while read -r _PKG_SIGN; do

        _PKG=${_PKG_SIGN%.asc}

        echo "Checking if $_PKG is already published."
        if is_published "$_PKG"; then
            echo "$_PKG is already published. Skipping."
            continue
        fi

        # download artifact from different pipeline
        buildkite-agent artifact download --build SOMETHING "$_PKG.asc" "$_PKG_DIR"
        mv "$_PKG_DIR/$_PKG.asc" "$_PKG_DIR/$_PKG.sig"
        buildkite-agent artifact upload "$_PKG_DIR/$_PKG.sig"
    done

}


case $CMD in
"--sign")
  upload_for_sign "$PACKAGE_DIR"
  ;;

"--publish")
  upload_for_publish "$PACKAGE_DIR"
  ;;

*)
  echo "Unknown command"
  ;;
esac