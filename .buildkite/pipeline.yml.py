#!/usr/bin/env python3

import json

build_agent = {
    "cpu": "2",
    "memory": "2G",
    "ephemeralStorage": "20G",
    "image": "golang:1.21-bookworm",
}

test_agent = {
    "provider": "gcp",
    "machineType": "n1-highmem-8",
    "assignExternalIP": False,
    "image": "family/elastic-buildkite-agent-ubuntu-2204-lts",
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
            "label": "Run static test",
            "depends_on": "build",
            "key": "static_test",
            "command": "echo do static test",
            #"agents": test_agent,
            "notify": [
                {
                    "github_commit_status": {
                        "context": "Buildkite Check Static Test",
                    },
                },
            ],
        },
        {
            "label": "Run pipeline test",
            "depends_on": "build",
            "key": "pipeline_test",
            "command": "echo do pipeline test",
            #"agents": test_agent,
            "notify": [
                {
                    "github_commit_status": {
                        "context": "Buildkite Check Pipeline Test",
                    },
                },
            ],
        },
        {
            "label": "Publish",
            "command": "echo Do publish when it is ready",
            "depends_on": [
                "static_test",
                "pipeline_test",
            ],
            "notify": [
                {
                    "github_commit_status": {
                        "context": "Buildktie Publish",
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
