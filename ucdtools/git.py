"""This module contains functions for cloning, committing, and pushing
collections of git repos.
"""
from datetime import datetime, timezone, timedelta
from getpass import getpass
from pathlib import Path

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


def clone_or_discover_repo(url, path, credentials = get_credentials()
        , use_cache = True):
    """This function clones a git repository from a URL.
    """
    # Create target directory if not already present.
    path = Path(path)
    path.mkdir(parents = True, exist_ok = True)

    repo_name = extract_repo_name(url)
    dest = path / repo_name

    if use_cache and dest.exists():
        repo = git.discover_repository(str(dest))
        print("Skipped '{}'".format(repo_name))
        return git.Repository(repo)

    callbacks = git.RemoteCallbacks(credentials = credentials)

    try:
        repo = git.clone_repository(url, str(dest), callbacks = callbacks)
        print("Cloned '{}'".format(repo_name))
        return repo

    except Exception as e:
        print("Failed to clone '{}'".format(repo_name))
        print("  {}".format(e))
        return None


def discover_repos(path):
    """Discover all repositories at the user-specified path.
    """
    path = Path(path)
    paths = (git.discover_repository(str(p)) for p in path.iterdir())
    return (git.Repository(p) for p in paths)


def commit_repo():
    """Given a list of repositories, this function adds files and creates a
    commit in each one.
    """
    pass


def push_repo():
    """Given a list of repositories, this function pushes commits in each
    one.
    """
    pass


def commit_feedback():
    author = pygit2.Signature(user, email)

    r.add("feedback.ipynb")
    r.index.write()
    tree = r.index.write_tree()


    oid = repository.create_commit("refs/head/master", author, author,
            "Add grader feedback.",
            tree, [repository.head.get_object().hex])


