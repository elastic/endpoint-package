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
import xxhash
import json

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.join(DIR_PATH, '..', '..')
PACKAGE_MANIFEST = os.path.join(ROOT, 'package', 'endpoint', 'manifest.yml')
VERSION_REGEX = re.compile('^version: (.*)')

LOCAL_REPO = git.Repo(ROOT)

UPSTREAM = 'upstream'
BACKPORT_FILE = os.path.join(ROOT, '.backportrc.json')


def print_capture(res):
    if res.stdout:
        click.echo(res.stdout)
    if res.stderr:
        click.echo(res.stderr)


def prompt_bump(current_version, released_branch):
    click.echo('Current version is: {}'.format(current_version))
    if released_branch != 'master':
        click.echo('Bumping the patch version because the base release branch was not master')
        part = 'patch'
    else:
        part = click.prompt('Bump which version part?', default='minor', type=click.Choice(['major', 'minor', 'patch'],
                                                                                           case_sensitive=False))
    res = subprocess.run(['bump2version', part], capture_output=True)
    print_capture(res)
    click.echo('New version: {}'.format(get_package_version()))


def bump_patch():
    res = subprocess.run(['bump2version', 'patch'], capture_output=True)
    print_capture(res)
    click.echo('New version: {}'.format(get_package_version()))


def bump_dev():
    click.echo('Bumping the build number')
    res = subprocess.run(['bump2version', 'build'], capture_output=True)
    print_capture(res)
    click.echo('New version: {}'.format(get_package_version()))


def bump_release():
    click.echo('Preparing for a release, removing the build number')
    res = subprocess.run(['bump2version', 'release'], capture_output=True)
    print_capture(res)
    click.echo('Version: {}'.format(get_package_version()))


def tag(repo, upstream, version):
    tag_name = 'v{}'.format(version)
    click.echo('Tagging endpoint version: {}'.format(tag_name))

    # remove old tag if it exists
    try:
        repo.git.tag(d=tag_name)
    except git.exc.GitCommandError as e:
        if 'not found' not in e.stderr:
            raise e

    try:
        repo.git.push(tag_name, d=upstream)
    except git.exc.GitCommandError as e:
        if 'remote ref does not exist' not in e.stderr:
            raise e

    repo.create_tag(tag_name)
    repo.git.push(upstream, tag_name)


def calc_dir_signature(dir_path):
    dir_signatures = []
    for root_dir, dirs, files in os.walk(os.path.abspath(os.path.expanduser(dir_path))):
        for filename in files:
            filepath = os.path.join(root_dir, filename)
            with open(filepath, 'rb') as f:
                dir_signatures.append(xxhash.xxh64_hexdigest(f.read()))
    dir_signatures.sort()
    sigs_as_string = '\n'.join(dir_signatures) + '\n'
    return xxhash.xxh64_hexdigest(sigs_as_string)


def create_pr(env, version, package_dir, package_storage_path):
    repo = git.Repo(package_storage_path)
    add_remote(repo, UPSTREAM, 'git@github.com:elastic/package-storage.git')
    branch_name = 'endpoint-release-{}'.format(version)
    delete_old_branch(repo, branch_name)
    repo.git.checkout(b=branch_name, t='{}/{}'.format(UPSTREAM, env))
    endpoint_path = os.path.join(package_storage_path, 'packages', 'endpoint')
    package_ver_path = os.path.join(endpoint_path, version)
    shutil.rmtree(package_ver_path, ignore_errors=True)
    os.makedirs(endpoint_path, exist_ok=True)

    click.echo('Copying package to: {}'.format(package_ver_path))
    ignored_patterns = shutil.ignore_patterns('_dev*')
    shutil.copytree(os.path.join(package_dir, 'endpoint') + os.path.sep, package_ver_path, ignore=ignored_patterns)
    repo.git.add(package_ver_path)
    repo.git.commit(m='Adding endpoint package version {}'.format(version))
    repo.git.push(branch_name, u='origin')

    dir_hash = calc_dir_signature(package_ver_path)
    click.echo('Endpoint package directory hash: {}'.format(dir_hash))

    click.echo('Creating PR to package-storage repo')
    res = subprocess.Popen(['hub', 'pull-request',
                            '-m', '[{}] Endpoint package version {}'.format(env, version),
                            '-m', 'Releasing new endpoint package',
                            '-m', 'endpoint/{} directory signature: {}'.format(version, dir_hash),
                            '-b', 'elastic:{}'.format(env), '-d'], cwd=package_storage_path,
                           stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout = res.stdout.read()
    if stdout:
        click.echo(stdout)
    stderr = res.stderr.read()
    if stderr:
        click.echo(stderr)


def get_package_version(include_dev=True):
    with open(PACKAGE_MANIFEST) as manifest:
        for line in manifest:
            line = line.rstrip()
            match = VERSION_REGEX.match(line)
            if match:
                if not include_dev:
                    return match.group(1).split('-')[0]
                else:
                    return match.group(1)
    raise Exception('Unable to find the package version')


def add_remote(repo, name, url):
    if name not in repo.remotes:
        remote = repo.create_remote(name, url)
    else:
        remote = repo.remote(name)
    remote.fetch(t=True)
    repo.git.remote('prune', name)
    return remote


def get_upstream_branch(repo):
    branches = [b.name.split('/')[1] for b in repo.remote(UPSTREAM).refs]
    upstream_branch = click.prompt('Which upstream branch should we release from?', default='master',
                                   type=click.Choice(branches))
    return upstream_branch


def delete_old_branch(repo, name, remote='origin'):
    # switch to a different branch before deleting
    repo.git.checkout('master')
    try:
        repo.git.branch(D=name)
    except git.exc.GitCommandError as e:
        if 'error: branch' not in e.stderr:
            raise e
    try:
        repo.git.push(name, d=remote)
    except git.exc.GitCommandError as e:
        if 'remote ref does not exist' not in e.stderr:
            raise e


def switch_to_bump_branch(repo, upstream_branch):
    branch_name = 'bump-version'
    delete_old_branch(repo, branch_name)
    repo.git.checkout(b=branch_name, t='{}/{}'.format(UPSTREAM, upstream_branch))
    return branch_name


def push_commits(repo, remote, local_branch, upstream_branch):
    click.echo('Pushing changes to upstream: {}'.format(upstream_branch))
    repo.git.push(remote, '{}:{}'.format(local_branch, upstream_branch))


def get_commit_hash(repo):
    return repo.head.object.hexsha


def get_release_branch(repo):
    while True:
        release_branch = click.prompt('What should the release branch name be?')
        remote_branches = [b.name.split('/')[1] for b in repo.remote(UPSTREAM).refs]
        if release_branch in remote_branches:
            click.echo('Release branch: {} already exists as a remote branch please create a new one')
        else:
            return release_branch


def update_backport(repo, release_branch, upstream_branch):
    # backporting only applies to commits that go to master so if the original release
    # was not targeting master then don't add anything to the .backportrc.json file
    if upstream_branch != 'master':
        return

    click.echo('Updating .backportrc.json file')
    branch_name = 'update-backport'
    delete_old_branch(repo, branch_name)
    repo.git.checkout(b=branch_name, t='{}/{}'.format(UPSTREAM, upstream_branch))
    with open(BACKPORT_FILE, 'r') as f:
        data = json.load(f)
    data['targetBranchChoices'].append(release_branch)
    with open(BACKPORT_FILE, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")

    repo.index.add([BACKPORT_FILE])
    repo.index.commit("adding {} to backport file".format(release_branch))
    push_commits(repo, UPSTREAM, branch_name, upstream_branch)


def handle_release_branch(repo, tagged_hash, upstream_branch):
    if not click.confirm('Should we create a branch to track this release?'):
        return
    release_branch = get_release_branch(repo)
    delete_old_branch(repo, release_branch)
    repo.git.checkout(tagged_hash, b=release_branch)
    bump_patch()
    push_commits(repo, UPSTREAM, release_branch, release_branch)
    update_backport(repo, release_branch, upstream_branch)


@click.command()
@click.argument('package_storage_path', type=click.Path(exists=True, file_okay=False, resolve_path=True),
                metavar='<path to package storage repo root directory>')
@click.argument('package_dir', type=click.Path(exists=True, file_okay=False, resolve_path=True),
                metavar='<path to the package directory in the endpoint-package repo>')
@click.option('--env', required=True, prompt='Is this a dev or prod release?', default='dev', type=click.Choice(
    ['dev', 'prod'], case_sensitive=False))
def main(package_storage_path, package_dir, env):
    click.echo('Current package version: {}'.format(get_package_version()))
    add_remote(LOCAL_REPO, UPSTREAM, 'git@github.com:elastic/endpoint-package.git')
    upstream_branch = get_upstream_branch(LOCAL_REPO)
    active_branch = LOCAL_REPO.active_branch
    if env == 'prod':
        branch_name = switch_to_bump_branch(LOCAL_REPO, upstream_branch)
        version = get_package_version(include_dev=False)
        bump_release()
        tag(LOCAL_REPO, UPSTREAM, version)
        # if we're going to create a new release branch to track this version of the stack we need the hash
        # after we have tagged the release version
        tagged_commit_hash = get_commit_hash(LOCAL_REPO)
        create_pr('snapshot', version, package_dir, package_storage_path)
        prompt_bump(version, upstream_branch)
        push_commits(LOCAL_REPO, UPSTREAM, branch_name, upstream_branch)
        handle_release_branch(LOCAL_REPO, tagged_commit_hash, upstream_branch)
    elif env == 'dev':
        branch_name = switch_to_bump_branch(LOCAL_REPO, upstream_branch)
        version = get_package_version()
        create_pr('snapshot', version, package_dir, package_storage_path)
        bump_dev()
        push_commits(LOCAL_REPO, UPSTREAM, branch_name, upstream_branch)
    else:
        click.echo('Invalid env option: {}'.format(env))
    LOCAL_REPO.git.checkout(active_branch)


if __name__ == '__main__':
    main()
