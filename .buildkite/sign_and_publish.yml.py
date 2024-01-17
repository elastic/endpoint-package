#!/usr/bin/env python3
#
# This script generates nested pipeline which isn't intended to be used alone.
#

import json
import argparse

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--depends-on", default=None, help="The key of the dependent step.")
    parser.add_argument("--group-name", default=None, help="The name of group that this pipeline is part of.")
    return parser.parse_args()


def main():
    args = parse_args()
    pipeline = {}
    steps = [
        {
            "label": "Trigger package sign",
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
            "artifact_paths": "artifacts-to-publish/*"
        },
        {
             "label": "Trigger publish sign",
             "trigger": "unified-release-gpg-signing",
             "depends_on": [
                 "download_signature",
             ],
             "skip": "Not Ready",
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
