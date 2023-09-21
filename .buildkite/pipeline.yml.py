#!/usr/bin/env python3

import json

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

def main():
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

    pipeline = {
        "steps": steps,
    }

    print(json.dumps(pipeline))


try:
    main()
except KeyboardInterrupt:
    pass
