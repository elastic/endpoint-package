#!/bin/bash
#
# The script upload package for signing and publishing.
#
# Usage:
#   upload.sh sign|publish <package_dir>
#

set -euo pipefail

CMD="${1:-unknown}"

#
# Print usage
#
print_usage() {
    echo "Usage: $(basename $0) Option"
    echo "    Option:"
    echo "        --check     Setup pipeline for signing and publish if"
    echo "                    generates artifact is not published."
    echo "        --publish   Publish if a given artifacts is not published."
}

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
# Generate signing and publishing pipieline if the package is not published
#
# $1 - Optional directory path for package upload. Default: artifacts-to-sign
#
check_if_published() {

    local _TMP_DIR _TO_SIGN_DIR _PKG_NAME _PKG_TO_SIGN_EXISTS
    _TO_SIGN_DIR="${1:-artifacts-to-sign}"
    _TMP_DIR="$(mktemp -d)"
    _PKG_TO_SIGN_EXISTS=false
    mkdir -p "$_TO_SIGN_DIR"

    echo "--- Download artifacts to check publish status"
    buildkite-agent artifact download "build/packages/*.zip" "$_TMP_DIR"

    while read -r _PKG; do

        _PKG_NAME=$(basename "$_PKG")
        echo "Checking if $_PKG_NAME is already published."
        if is_published "$_PKG_NAME"; then
            echo "$_PKG_NAME is already published. Skipping."
            continue
        fi

        echo "$_PKG_NAME is unpublished. Preparing for signing."

        mv "$_PKG" "$_TO_SIGN_DIR"
        _PKG_TO_SIGN_EXISTS=true

    done <<< "$( find "$_TMP_DIR" -name "*.zip" | sort )"

    if $_PKG_TO_SIGN_EXISTS; then
        echo "--- Generating pipeline for signing and publishing"
        python3 .buildkite/sign_and_publish.yml.py \
            --depends-on "$BUILDKITE_STEP_KEY" | buildkite-agent pipeline upload
    fi

}


#
# Upload package and signature file for publish if not published already
#
# $1 - Optional directory path for package upload. Default: artifacts-to-publish
#
upload_for_publish() {

    local _TMP_DIR _TO_PUBLISH_DIR _PKG_NAME
    _TO_PUBLISH_DIR="${1:-artifacts-to-publish}"
    _TMP_DIR="$(mktemp -d)"
    mkdir -p "$_TO_PUBLISH_DIR"

    echo "--- Performing buildkite-agent step get"
    BUILDKITE_API_TOKEN="$(vault kv get -field=token secret/ci/elastic-endpoint-package/buildkite)"
    export BUILDKITE_API_TOKEN
    ARTIFACTS_BUILD_ID=$(python .buildkite/scripts/build_info.py --step-key package_sign --print-triggered-build-id)

    echo "--- Downloading signature to check publishing status"
    buildkite-agent artifact download "*.asc" "$_TMP_DIR" --build "${ARTIFACTS_BUILD_ID}"

    while read -r _PKG_SIGN; do

        _PKG_NAME=$(basename "${_PKG_SIGN%.asc}")

        echo "Checking if $_PKG_NAME is already published."
        if is_published "$_PKG_NAME"; then
            echo "$_PKG is already published. Skipping."
            continue
        fi

        echo "Downloading $_PKG_NAME for publishing."
        buildkite-agent artifact download "build/packages/$_PKG_NAME" ./
        mv "build/packages/$_PKG_NAME" "$_TO_PUBLISH_DIR/"

        echo "Moving signature $_PKG_SIGN for publishing."
        mv "$_PKG_SIGN" "$_TO_PUBLISH_DIR/"

    done <<< "$(find "$_TMP_DIR" -name "*.asc" | sort )"

}


case $CMD in
"--check")
  check_fi_published artifacts-to-sign
  ;;

"--publish")
  upload_for_publish artifacts-to-publish
  ;;

*)
  echo "Unknown command"
  print_usage
  exit 1
  ;;
esac