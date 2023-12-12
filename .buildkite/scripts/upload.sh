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

    local _TMP_DIR _TO_SIGN_DIR _PKG_NAME
    _TO_SIGN_DIR="${1:-artifacts-to-sign}"
    _TMP_DIR="$(mktemp -d)"
    mkdir -p "$_TO_SIGN_DIR"

    echo "--- Download artifacts to check publish status"
    buildkite-agent artifact download "build/packages/*.zip" "$_TMP_DIR"

    find "$_TMP_DIR" -name "*.zip" | sort | while read -r _PKG; do

        _PKG_NAME=$(basename "$_PKG")
        echo "Checking if $_PKG_NAME is already published."
        if is_published "$_PKG_NAME"; then
            echo "$_PKG_NAME is already published. Skipping."
            continue
        fi

        mv "$_PKG" "$_TO_SIGN_DIR"

    done

}


#
# Upload package and signature file for publish
#
upload_for_publish() {

    local _TMP_DIR _TO_PUBLISH_DIR _PKG_NAME
    _TO_PUBLISH_DIR="${1:artifacts-to-publish}"
    _TMP_DIR="$(mktemp -d)"
    mkdir -p "$_TO_PUBLISH_DIR"

    echo "--- Performing buildkite-agent step get"
    ARTIFACTS_BUILD_ID=$(python .buildkite/scripts/build_info.py --step-key package_sign --print-triggered-build-id)

    echo "--- Downloading signature to check publishing status"
    buildkite-agent artifact download "*.asc" "$_TMP_DIR" --build "${ARTIFACTS_BUILD_ID}"

    find "$_PKG_DIR" -name "*.asc" | sort | while read -r _PKG_SIGN; do

        _PKG_NAME=$(basename "${_PKG_SIGN%.asc}.zip")

        echo "Checking if $_PKG_NAME is already published."
        if is_published "$_PKG_NAME"; then
            echo "$_PKG is already published. Skipping."
            continue
        fi

        echo "Downloading $_PKG_NAME for publishing."
        buildkite-agent artifact download "build/packages/$_PKG_NAME" "$_TO_PUBLISH_DIR"

        mv "$_PKG_SIGN" "$_PKG_DIR/"
    done

}


case $CMD in
"--sign")
  upload_for_sign artifacts-to-sign
  ;;

"--publish")
  upload_for_publish artifacts-to-publish
  ;;

*)
  echo "Unknown command"
  ;;
esac