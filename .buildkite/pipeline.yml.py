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

    # if current_branch == "main" or re.match(r"^[78]\.\d+$", current_branch):
    if current_branch == "bk/sign":
        steps.extend([
            {
                "wait": None
            },
            {
                "label": "Check publish status",
                "command": ".buildkite/scripts/upload.sh --sign",
                "key": "check_for_sign",
                # This artifact_paths is required by the gpg signinig pipeline.
                "artifact_paths": "artifacts-to-sign/*.zip"
            },

        ])

    pipeline = {
        "steps": steps,
    }

    print(json.dumps(pipeline))


try:
    main()
except KeyboardInterrupt:
    pass
