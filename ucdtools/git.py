"""This module contains functions for cloning, committing, and pushing
collections of git repos.
"""
from datetime import datetime, timezone, timedelta
from getpass import getpass
from pathlib import Path
import shutil

import pygit2 as git


def check_late(repo, deadline):
    """Check whether the latest commit in a repository is past the deadline.
    """
    head = repo.get(repo.head.target)
    path = Path(repo.path).parent.name

    tzinfo = timezone(timedelta(minutes = head.author.offset))
    timestamp = datetime.fromtimestamp(float(head.author.time), tzinfo)

    is_late = timestamp > deadline
    if is_late:
        print("Late ({}): {}".format(path, timestamp))

    return is_late


def extract_repo_name(url):
    return url.rpartition("/")[-1].rpartition(".")[0]


def get_credentials(use_ssh = True):
    """This function gets git credentials for the user.
    """
    if use_ssh:
        cred = git.KeypairFromAgent("git")
    else:
        username = input("Username: ")
        password = getpass("Password: ")
        cred = git.UserPass(username, password)

    return cred


def discover_repos(path):
    """Discover all repositories at the user-specified path.
    """
    path = Path(path)
    paths = (git.discover_repository(str(p)) for p in path.iterdir())
    return (git.Repository(p) for p in paths)


def clone(url, dest, credentials = get_credentials(), use_cache = True):
    """This function clones a git repository from a URL.
    """
    dest = Path(dest)

    if dest.exists():
        if use_cache:
            repo = git.discover_repository(str(dest))
            print("Skipped '{}'".format(dest))
            return git.Repository(repo)
        else:
            shutil.rmtree(dest)

    callbacks = git.RemoteCallbacks(credentials = credentials)

    try:
        repo = git.clone_repository(url, str(dest), callbacks = callbacks)
        print("Cloned '{}'".format(dest))
        return repo

    except Exception as e:
        print("Failed to clone '{}'".format(dest))
        print("  {}".format(e))
        return None


def add(repo, path):
    """Add a file to the staging area of a repo.
    """
    repo.index.add(path)
    repo.index.write()


def commit(repo, message, author = None, ref = "refs/heads/master"):
    """Commit a repo.
    """
    if not author:
        author = repo.default_signature

    tree = repo.index.write_tree()

    oid = repo.create_commit(ref, author, author, message, tree,
            [repo.head.get_object().hex])

    repo.head.set_target(oid)

    return oid


def push(repo, credentials = get_credentials(), remote = None,
        ref = "refs/heads/master"):
    """Given a list of repositories, this function pushes commits in each
    one.
    """
    if not remote:
        remote = repo.remotes["origin"]

    callbacks = git.RemoteCallbacks(credentials = credentials)

    remote.push([ref], callbacks)
