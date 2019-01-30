#!/usr/bin/env python3
"""This module clones all of the student repositories for a given assignment.

To use this as a script, run

    python clone_hw.py NAME OUT

where NAME is the assignment name and OUT is the directory to clone into.
"""
import argparse
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd

import config as cfg
import ucdtools.git as git
import ucdtools.notebook as note


def do_clone(args):
    """This subprogram clones all repositories for the user-specified
    assignment, by combining the base URL, the assignment name, and each
    username.
    """
    roster = pd.read_csv(args.users)

    base_url = urljoin(cfg.base_url, args.name)
    use_ssh = base_url.startswith("git")
    cred = git.get_credentials(use_ssh)

    # Create dest directory if not already present.
    dest = Path(args.dest)
    dest.mkdir(parents = True, exist_ok = True)

    print("Cloning repositories...")
    for email, user in roster.itertuples(index = False):
        url = "{}-{}.git".format(base_url, user)

        repo_dest = dest / email.partition("@")[0]

        git.clone(url, repo_dest, cred, args.use_cache)


def do_grade(args):
    """This subprogram prepares all repositories in a directory for grading.
    There are two steps for each repo:
    
    1. Print names of repos where the latest commit is after the due date.
    2. Create a 'feedback.ipynb' file from the homework file.
    """
    due = datetime.strptime(args.due, "%m.%d %H:%M")
    due = due.replace(year = cfg.year, tzinfo = cfg.tzinfo)

    repos = git.discover_repos(args.path)

    for repo in repos:
        git.check_late(repo, due)
        note.init_feedback(Path(repo.path).parent)


def do_commit(args):
    """This subprogram adds and commits a user-specified file for all
    repositories in a directory.
    """
    repos = git.discover_repos(args.path)

    for repo in repos:
        git.add(repo, args.file)
        git.commit(repo, args.message)


def do_push(args):
    """This subprogram pushes to 'origin/master' for all repositories in a
    directory.
    """
    repos = git.discover_repos(args.path)

    use_ssh = cfg.base_url.startswith("git")
    cred = git.get_credentials(use_ssh)

    for repo in repos:
        git.push(repo, cred)


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(help = "action to take", required = True,
            dest = "subcommand")

    # Clone Tool Arguments ----------------------------------------
    p_clone = sp.add_parser("clone")
    p_clone.add_argument("dest", help = "path to output directory")
    p_clone.add_argument("name", help = "name of assignment")
    p_clone.add_argument("users", help = "path to usernames file",
            default = cfg.users, nargs = "?")
    p_clone.add_argument("--overwrite", dest = "use_cache",
            action = "store_false", help = "overwrite cached repositories")
    p_clone.set_defaults(subprogram = do_clone)

    # Grade Tool Arguments ----------------------------------------
    p_grade = sp.add_parser("grade")
    p_grade.add_argument("path", help = "path to repositories directory")
    p_grade.add_argument("due", help = "due date in 'MM.DD hh:mm' format")
    p_grade.set_defaults(subprogram = do_grade)

    # Commit Tool Arguments ----------------------------------------
    p_commit = sp.add_parser("commit")
    p_commit.add_argument("path", help = "path to repositories directory")
    p_commit.add_argument("file", help = "name of file to commit")
    p_commit.add_argument("message", help = "commit message")
    p_commit.set_defaults(subprogram = do_commit)

    # Push Tool Arguments ----------------------------------------
    p_push = sp.add_parser("push")
    p_push.add_argument("path", help = "path to repositories directory")
    p_push.set_defaults(subprogram = do_push)

    # Parse arguments and run subprogram
    args = ap.parse_args()
    args.subprogram(args)


if __name__ == "__main__":
    main()
