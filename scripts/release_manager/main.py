#
# Copyright Elasticsearch B.V. and/or licensed to Elasticsearch B.V. under one
# or more contributor license agreements. Licensed under the Elastic License;
# you may not use this file except in compliance with the Elastic License.
#

import click
import subprocess
import os
import re
import git
import shutil

dir_path = os.path.dirname(os.path.realpath(__file__))
root = os.path.join(dir_path, '..', '..')
package_manifest = os.path.join(root, 'package', 'endpoint', 'manifest.yml')
version_regex = re.compile('^version: (.*)')

local_repo = git.Repo(root)

UPSTREAM = 'upstream'


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
    tag_name = 'v{}'.format(version)
    repo.create_tag(tag_name)
    git_cmd = repo.git
    git_cmd.push(upstream, tag_name)


def create_pr(env, version, package_dir, package_storage_path):
    repo = git.Repo(package_storage_path)
    add_remote(repo, UPSTREAM, 'git@github.com:elastic/package-storage.git')
    branch_name = 'endpoint-release-{}'.format(version)

    delete_old_branch(repo, branch_name)

    repo.git.checkout(b=branch_name, t='{}/{}'.format(UPSTREAM, env))
    endpoint_path = os.path.join(package_storage_path, 'package', 'endpoint')
    package_ver_path = os.path.join(endpoint_path, version)
    shutil.rmtree(package_ver_path, ignore_errors=True)
    os.makedirs(endpoint_path, exist_ok=True)
    shutil.copytree(os.path.join(package_dir, 'endpoint') + os.path.sep, package_ver_path)
    repo.git.add(package_ver_path)
    repo.git.commit(m='Adding endpoint package version {}'.format(version))
    repo.git.push(branch_name, u='origin')

    click.echo('Creating PR to package-storage repo')
    res = subprocess.Popen(['hub', 'pull-request',
                            '-m', '[{}] Endpoint package version {}'.format(env, version),
                            '-m', 'Releasing new endpoint package',
                            '-b', 'elastic:{}'.format(env), '-d'], cwd=package_storage_path,
                           stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    print_capture(res)


def get_package_version(no_dev=False):
    with open(package_manifest) as manifest:
        for line in manifest:
            line = line.rstrip()
            match = version_regex.match(line)
            if match:
                if no_dev:
                    return match.group(1).split('-')[0]
                else:
                    return match.group(1)
    raise Exception('Unable to find the package version')


def add_remote(repo, name, url):
    if name not in repo.remotes:
        remote = repo.create_remote(name, url)
    else:
        remote = repo.remote(name)
    remote.fetch()
    return remote


def get_upstream_branch(repo):
    branches = [b.name.split('/')[1] for b in repo.remote(UPSTREAM).refs]
    upstream_branch = click.prompt('Which upstream branch should we release from?', default='master',
                                   type=click.Choice(branches))
    return upstream_branch


def delete_old_branch(repo, name, remote='origin'):
    try:
        repo.git.branch(D=name)
    except git.exc.GitCommandError:
        pass
    try:
        repo.git.push(name, d=remote)
    except git.exc.GitCommandError:
        pass


def switch_to_bump_branch(repo, version, upstream_branch):
    branch_name = 'bump-version-{}'.format(version)
    delete_old_branch(repo, branch_name)
    repo.git.checkout(b=branch_name, t='{}/{}'.format(UPSTREAM, upstream_branch))
    return branch_name


def push_commits(repo, remote, local_branch, upstream_branch):
    repo.git.push(remote, '{}:{}'.format(local_branch, upstream_branch))


@click.command()
@click.argument('package_storage_path', type=click.Path(exists=True, file_okay=False, resolve_path=True), metavar='<path to package storage repo root directory>')
@click.argument('package_dir', type=click.Path(exists=True, file_okay=False, resolve_path=True), metavar='<path to the package directory in the endpoint-package repo>')
@click.confirmation_option(
    prompt='Current branch is {} do you wish to continue with the release?'.format(local_repo.active_branch))
@click.option('--env', required=True, prompt='Is this a dev or prod release?', default='dev', type=click.Choice(
    ['dev', 'prod'], case_sensitive=False))
def main(package_storage_path, package_dir, env):
    click.echo('env: {}'.format(env))
    add_remote(local_repo, UPSTREAM, 'git@github.com:elastic/endpoint-package.git')
    upstream_branch = get_upstream_branch(local_repo)

    if env == 'prod':
        version = get_package_version(no_dev=True)
        branch_name = switch_to_bump_branch(local_repo, version, upstream_branch)
        bump_release()
        tag(local_repo, UPSTREAM, version)
        create_pr('production', version, package_dir, package_storage_path)
        prompt_bump()
        push_commits(local_repo, UPSTREAM, branch_name, upstream_branch)
    elif env == 'dev':
        version = get_package_version()
        branch_name = switch_to_bump_branch(local_repo, version, upstream_branch)
        create_pr('snapshot', version, package_dir, package_storage_path)
        bump_dev()
        push_commits(local_repo, UPSTREAM, branch_name, upstream_branch)
    else:
        click.echo('Invalid env option: {}'.format(env))


if __name__ == '__main__':
    main()