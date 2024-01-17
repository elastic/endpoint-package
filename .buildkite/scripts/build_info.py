import argparse
import os
import requests
import sys

_BUILDKITE_API_URL = "https://api.buildkite.com/v2/organizations/elastic/pipelines/{pipeline_slug}/builds/{build_number}"


def get_build_json(api_token, pipeline_slug, build_number):
    if api_token is None or len(api_token) == 0:
        raise Exception('Missing API token')
    if pipeline_slug is None or len(pipeline_slug) == 0:
        raise Exception('Missing pipeline slug')
    if build_number is None or len(build_number) == 0:
        raise Exception('Missing build number')

    resp = requests.get(
        url=_BUILDKITE_API_URL.format(
            pipeline_slug=pipeline_slug, build_number=build_number),
        headers={"Authorization": f"Bearer {api_token}"},
    )

    resp.raise_for_status()

    return resp.json()


def get_step_json(api_token, pipeline_slug, build_number, step_key):
    if api_token is None or len(api_token) == 0:
        raise Exception('Missing API token')
    if pipeline_slug is None or len(pipeline_slug) == 0:
        raise Exception('Missing pipeline slug')
    if build_number is None or len(build_number) == 0:
        raise Exception('Missing build number')
    if step_key is None or len(step_key) == 0:
        raise Exception('Missing step key')

    build_json = get_build_json(api_token, pipeline_slug, build_number)

    step_json = None
    for step in build_json['jobs']:
        if ('step_key' in step.keys() and step['step_key'] == step_key):
            step_json = step
            break

    if step_json is None:
        raise Exception('Step [%s] not found' % step_key)

    return step_json


def main():
    parser = argparse.ArgumentParser(
        description="Queries build for specific values")
    parser.add_argument("--print-build-json",
                        required=False,
                        action='store_true',
                        help='Print the build information as json.')
    parser.add_argument("--print-step-json",
                        required=False,
                        action='store_true',
                        help='Print the step json for --step-key')
    parser.add_argument("--print-triggered-build-number",
                        required=False,
                        action='store_true',
                        help='Print the triggered build number')
    parser.add_argument("--print-triggered-build-id",
                        required=False,
                        action='store_true',
                        help='Print the triggered build id')
    parser.add_argument("--print-triggered-pipeline",
                        required=False,
                        action='store_true',
                        help='Print the triggered pipeline name')
    parser.add_argument("--build-number",
                        required=False,
                        default=os.getenv("BUILDKITE_BUILD_NUMBER", ""),
                        help='The build number')
    parser.add_argument("--pipeline-slug",
                        required=False,
                        default=os.getenv("BUILDKITE_PIPELINE_SLUG", ""),
                        help='The pipeline slug')
    parser.add_argument("--api-token",
                        required=False,
                        default=os.getenv("BUILDKITE_API_TOKEN", ""),
                        help='The Buildkite API token')
    parser.add_argument("--step-key",
                        required=False,
                        default=None,
                        help='The step key to query')

    args = parser.parse_args()

    if (args.print_build_json):
        print(get_build_json(args.api_token, args.pipeline_slug, args.build_number))
    if (args.print_step_json):
        print(get_step_json(args.api_token, args.pipeline_slug, args.build_number, args.step_key))
    if (args.print_triggered_build_number):
        step_json = get_step_json(args.api_token, args.pipeline_slug, args.build_number, args.step_key)

        try:
            print(step_json['triggered_build']['number'])
        except:
            raise Exception("Invalid step_key (not a trigger step)")
    if (args.print_triggered_pipeline):
        step_json = get_step_json(args.api_token, args.pipeline_slug, args.build_number, args.step_key)

        try:
            print(step_json['triggered_build']['url'].split('/')[7])
        except:
            raise Exception("Invalid step_key (not a trigger step)")
    if (args.print_triggered_build_id):
        step_json = get_step_json(args.api_token, args.pipeline_slug, args.build_number, args.step_key)

        try:
            print(step_json['triggered_build']['id'])
        except:
            raise Exception("Invalid step_key (not a trigger step)")


if __name__ == "__main__":
    sys.exit(main())
