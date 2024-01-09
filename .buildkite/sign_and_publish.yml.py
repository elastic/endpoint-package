#!/usr/bin/env python3
#
# This script generates nested pipeline which isn't intended to be used alone.
#

import argparse
import json
import os

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--depends-on", default=None, help="The key of the dependent step.")
    parser.add_argument("--group-name", default=None, help="The name of group that this pipeline is part of.")
    return parser.parse_args()


def main():
    args = parse_args()
    # This only gets triggered when the branch is either main or 7.\d or 8.\d
    # So, dry_run is true for non main branch
    branch = os.getenv("BUILDKITE_BRANCH")
    dry_run = branch != "main"
    pipeline = {}
    steps = [
        {
            "label": f"Trigger package sign for endpoint-package {branch} branch",
            "trigger": "unified-release-gpg-signing",
            "key": "package_sign",
            "depends_on": [],
            "build": {
                "env": {
                    "INPUT_PATH": "buildkite://",
                },
            },
        },
        {
            "label": "Prepare package for publish",
            "command": ".buildkite/scripts/sign_and_publish.sh --publish",
            "key": "download_signature",
            "depends_on": [
                "package_sign",
            ],
            "artifact_paths": "packageArtifacts/*"
        },
        {
             "label": f"Trigger publishing for endpoint-package {branch} branch",
             "trigger": "package-storage-infra-publishing",
             "depends_on": [
                 "download_signature",
             ],
            "build": {
                "env": {
                    "DRY_RUN": "true" if dry_run else "false",
                    # From legacy Jenkins pipeline:
                    #   FIXME legacy_package=false
                    #   endpoint-package must be aligned with spec first, this option disables validation on the job side
                    "LEGACY_PACKAGE": "true",
                    "PACKAGE_ARTIFACTS_FOLDER": "packageArtifacts"
                },
            },
        },
    ]

    if args.depends_on:
        for each in steps:
            each["depends_on"].append(args.depends_on)

    if args.group_name:
        steps = {
            "group": args.group_name,
            "steps": steps,
        }
    pipeline = {
        "steps": steps
    }

    print(json.dumps(pipeline))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
