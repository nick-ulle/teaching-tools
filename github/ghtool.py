#!/usr/bin/env python3

import argparse
from itertools import chain
import getpass
from pathlib import Path
import sys

import github

GH_ORG = "UCDSTA141B"
ADMINS = ["jsharpna", "Chunjui", "nick-ulle"]

def read_token(path = "token"):
    path = Path(path)
    if not path.is_file():
        print(
            f"Please put your GitHub token in a plaintext file named '{path}'."
        )
        sys.exit(1)

    with open(path, "rt") as f:
        return f.readline().strip()

TOKEN = read_token()


def get_user_logins(org):
    users = chain(org.get_members(), org.get_outside_collaborators())
    return sorted(u.login for u in users)


def prompt(message):
    """Prompt user for a y/n answer."""
    while True:
        response = input(message + " [y/n]: ")
        if response == "y":
            return True
        elif response == "n":
            return False


def gh_fetch_file(args):
    """Fetch a file from all org repositories that match the search term."""
    path = args.path
    search = args.search

    out_dir = Path(args.target)
    if not out_dir.is_dir():
        out_dir.mkdir()
    elif not prompt(f"'{out_dir}' already exists. Continue?"):
        return None
    
    org = github.Github(TOKEN).get_organization(GH_ORG)
    repos = (r for r in org.get_repos() if search in r.name)
    
    students = [s for s in get_user_logins(org) if s not in ADMINS]

    print("Found notebooks:")
    for repo in repos:
        # Figure out which students use this repo.
        repo_users = [
            u.login for u in repo.get_collaborators()
            if u.login not in ADMINS
        ]
        if len(repo_users) == 0:
            # FIXME: This skips students that commit without setting up their
            # git email.
            continue

        # Find the file.
        try:
            content = repo.get_contents(path)
        except github.GithubException as exc:
            if "too large" in exc.data.get("message", ""):
                print(f"Large '{path}' ({repo.html_url})")
            else:
                print(f"No '{path}' ({repo.html_url})")
            continue

        # Remove them from the list of students.
        students = [s for s in students if s not in repo_users]

        name = "_".join(repo_users) + ".ipynb"
        with open(out_dir / name, "wb") as f:
            f.write(content.decoded_content)
        print(f"{name} ({repo.html_url})")

    if len(students) != 0:
        print("\nNo notebook found for:")
        print("\n".join(students))

    print("\nFinished!")


# ------------------------------------------------------------
# Monkey-patch a method for getting outside collaborators.
# Based on PyGithub PR #533 from @jappievw.
def get_outside_collaborators(self, filter_=github.GithubObject.NotSet):
    """
    :calls: `GET /orgs/:org/outside_collaborators <http://developer.github.com/v3/orgs/outside_collaborators>`_
    :param filter_: string
    :rtype: :class:`github.PaginatedList.PaginatedList` of :class:`github.NamedUser.NamedUser`
    """
    assert (filter_ is github.GithubObject.NotSet or
            isinstance(filter_, (str, unicode))), filter_

    url_parameters = {}
    if filter_ is not github.GithubObject.NotSet:
        url_parameters["filter"] = filter_
    return github.PaginatedList.PaginatedList(
        github.NamedUser.NamedUser,
        self._requester,
        self.url + "/outside_collaborators",
        url_parameters
    )

github.Organization.Organization.get_outside_collaborators = (
    get_outside_collaborators
)
# ------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(help = "action to take")

    # Fetch Tool Arguments ----------------------------------------
    p_fetch = sp.add_parser("fetch")
    p_fetch.add_argument("path", help = "file to fetch")
    p_fetch.add_argument("search", nargs = "?", default = "",
        help = "term to require in repo name")
    p_fetch.add_argument("target", nargs = "?", default = "submissions",
        help = "path to output directory")
    p_fetch.set_defaults(subprogram = gh_fetch_file)

    # Parse arguments and run subprogram
    args = ap.parse_args()
    args.subprogram(args)


if __name__ == "__main__":
    main()
