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

    if current_branch == "main" or current_branch == "8.x" or re.match(r"^[7-9]\.\d+$", current_branch):
        steps.append({
                "label": "Check if published",
                "command": ".buildkite/scripts/sign_and_publish.sh --check",
                "key": "check_for_sign",
                "depends_on": [
                    "build",
                    "check",
                ],
                # This artifact_paths is required by the gpg signinig pipeline.
                "artifact_paths": "artifacts-to-sign/*.zip"
        })

    pipeline = {
        "env": {
            "USE_HTTPS_CLONE": True,
        },
        "steps": steps,
    }

    print(json.dumps(pipeline))


try:
    main()
except KeyboardInterrupt:
    pass
