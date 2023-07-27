import json

def main():
    return json.dumps({
        "steps": [
            {
                "label": "Hello Buildkite",
                "command": "echo Hello Buildkite",
            },
        ]
    })
try:
    main()
except KeyboardInterrupt:
    pass