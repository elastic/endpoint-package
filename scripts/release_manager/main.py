#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License;
# you may not use this file except in compliance with the Elastic License.
#

import argparse
import subprocess
import glob
import os
import shutil
import sys
import click
import subprocess
import os
import re
import git

dir_path = os.path.dirname(os.path.realpath(__file__))
root = os.path.join(dir_path, '..', '..')
package_manifest = os.path.join(root, 'package', 'endpoint', 'manifest.yml')
version_regex = re.compile('^version: (.*)')


def print_capture(res):
    click.echo(res.stdout)
    click.echo(res.stderr)


def prompt_bump():
    part = click.prompt('Bump which version part?', default='minor', type=click.Choice(['major', 'minor', 'patch'],
                                                                                       case_sensitive=False))
    click.echo('part: {}'.format(part))
    res = subprocess.run(['bump2version', part], capture_output=True)
    print_capture(res)


def bump_dev():
    click.echo('Bumping the build number')
    res = subprocess.run(['bump2version', 'build'], capture_output=True)
    print_capture(res)


def bump_release():
    click.echo('Preparing for a release, removing the build number')
    res = subprocess.run(['bump2version', 'release'], capture_output=True)
    print_capture(res)


def tag(repo, upstream, version):
    repo.create_tag('v{}'.format(version))


def push_commit():
    pass


def create_pr(env, version):
    click.echo('Creating PR to package-storage repo')
    res = subprocess.run(['hub', 'pull-request',
                          '-m', '[{}] Endpoint package version {}'.format(env, version),
                          '-m', 'Releasing new endpoint package',
                          '-b', 'elastic:{}'.format(env), '-d'], capture_output=True)
    print_capture(res)


def get_package_version():
    with open(package_manifest) as manifest:
        for line in manifest:
            line = line.rstrip()
            match = version_regex.match(line)
            if match:
                return match.group(1)


@click.command()
@click.option('--env', required=True, prompt='Is this a dev or prod release?', default='dev', type=click.Choice(
    ['dev', 'prod'], case_sensitive=False))
def main(env):
    click.echo('env: {}'.format(env))
    repo = git.Repo(root)
    upstream = repo.create_remote('upstream', 'git@github.com:elastic/endpoint-package.git')

    if env == 'prod':
        # switch branch
        bump_release()
        version = get_package_version()
        if not version:
            pass
            # display error
        tag(repo, upstream, version)

        create_pr('production', version)
        prompt_bump()
        push_commit()
    elif env == 'dev':
        version = get_package_version()
        if not version:
            pass
            # throw error
        # switch branch
        create_pr('snapshot', version)
        bump_dev()
        push_commit()
    else:
        click.echo('Invalid env option: {}'.format(env))


if __name__ == '__main__':
    main()
