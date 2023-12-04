#!/usr/bin/env python3

import json
import os
import re

build_agent = {
    "cpu": "2",
    "memory": "4G",
    "ephemeralStorage": "10G",
    "image": "golang:1.21-bookworm",
}

test_agent = {
    "provider": "gcp",
    "machineType": "n1-highmem-8",
    "assignExternalIP": False,
    "image": "family/core-ubuntu-2204",
}

publish_agent = {
    "image": "google/cloud-sdk:slim",
}


def main():
    current_branch = os.getenv("BUILDKITE_BRANCH")
    steps = []
    """
    steps = [
        {
            "label": "Build",
            "command": ".buildkite/scripts/build.sh",
            "key": "build",
            "agents": build_agent,
            "artifact_paths": [
                "build/packages/*.zip",
            ],
            "notify": [
                {
                    "github_commit_status": {
                        "context": "Buildkite Build",
                    },
                },
            ],
        },
        {
            "label": "Run Static and Pipeline check",
            "key": "check",
            "command": ".buildkite/scripts/check.sh",
            "agents": test_agent,
            "notify": [
                {
                    "github_commit_status": {
                        "context": "Buildkite Check",
                    },
                },
            ],
        },
    ]
    """

    #if current_branch == "main" or re.match(r"^[78]\.\d+$", current_branch):
    if current_branch == "bk/sign":
        steps.append({
            "group": "Publish",
            "steps": [
                {
                    "label": "Upload unpublished package",
                    "command": ".buildkite/scripts/publish.py build/packages",
                    "key": "upload_for_sign",
                },
                {
                    "label": "Trigger package sign",
                    "trigger": "unified-release-gpg-signing",
                    "depends_on": "upload_for_sign",
                    "key": "package_sign",
                },
                {
                    "label": "Download package signature",
                    "command": ".buildkite/scripts/publish.py build/packages",
                    "depends_on": "package_sign",
                    "key": "package_sign",
                },
                {
                    "label": "Upload for publish",
                    "command": ".buildkite/scripts/publish.py build/packages",
                    "key": "upload_for_publish",
                    "depends_on": "package_sign"
                },
                # {
                #     "label": "Trigger publish sign",
                #     "trigger": "unified-release-gpg-signing",
                #     "depends_on": "upload_for_publish",
                # },
            ],
            "depends_on": [
                "check",
                "build",
            ]
        })

    pipeline = {
        "steps": steps,
    }

    print(json.dumps(pipeline))


try:
    main()
except KeyboardInterrupt:
    pass
