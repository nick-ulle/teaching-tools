#!/usr/bin/env python3

# Fetch the student hw5 repos

import base64
from pathlib import Path

import github

from ghtool import TOKEN, GH_ORG, ADMINS, get_user_logins

SEARCH = "hw5"

MISSING = [
        # Missing accounts go here
]

def fork():
    path = "hw5.ipynb"
    out_dir = Path("hw5")
    students = MISSING.copy()

    gh = github.Github(TOKEN)

    james = gh.get_user("jsharpna")
    origin_repo = james.get_repo("sta141b-hw5")

    for fork in origin_repo.get_forks():
        name = fork.owner.login

        # Check that the repo has commits.
        try:
            hashes = [x.sha for x in fork.get_commits()]
            if hashes[0] == "fdb8f971eae992ec1f723bcc38019f257b869f68":
                print(f"  No change ({fork.html_url})")
                continue
        except github.GithubException as exc:
            print(f"  No commits ({fork.html_url})")
            continue

        # Find the file.
        contents = fork.get_dir_contents("/")
        contents = [x for x in contents if x.path == path]
        if len(contents) == 0:
            print(f"  No '{path}' ({fork.html_url})")
            continue

        blob = fork.get_git_blob(contents[0].sha)
        blob = bytearray(blob.content, "utf-8")
        content = base64.b64decode(blob)

        # Remove them from the list of students.
        students = [s for s in students if s != name]

        # Write to disk.
        name = name + ".ipynb"
        fname = out_dir / name
        if fname.exists():
            with open(fname, "rb") as f:
                old_content = f.read()
            if old_content == content:
                print(f"{name} ({fork.html_url})")
            else:
                print(f"  Exists: '{path}' ({fork.html_url})")
            continue

        with open(fname, "wb") as f:
            f.write(content)
        print(f"{name} ({fork.html_url})")

    if len(students) != 0:
        print("\nNo notebook found for:")
        print("\n".join(students))

    print("\nFinished!")


def main():
    path = "hw5.ipynb"
    out_dir = Path("hw5")

    gh = github.Github(TOKEN)
    org = gh.get_organization(GH_ORG)
    students = [s for s in get_user_logins(org) if s not in ADMINS]

    # First try to get the hw5 repos from the org.
    repos = (r for r in org.get_repos() if SEARCH in r.name)

    print("Found notebooks:")
    for repo in repos:
        # Figure out which students use this repo.
        repo_users = [
            u.login for u in repo.get_collaborators()
            if u.login not in ADMINS
        ]
        if len(repo_users) == 0:
            continue

        # Check that the repo has commits.
        try:
            hashes = [x.sha for x in repo.get_commits()]
            if hashes[0] == "fdb8f971eae992ec1f723bcc38019f257b869f68":
                print(f"  No change ({repo.html_url})")
                continue
        except github.GithubException as exc:
            print(f"  No commits ({repo.html_url})")
            continue

        # Find the file.
        contents = repo.get_dir_contents("/")
        contents = [x for x in contents if x.path == path]
        if len(contents) == 0:
            print(f"  No '{path}' ({repo.html_url})")
            continue

        blob = repo.get_git_blob(contents[0].sha)
        blob = bytearray(blob.content, "utf-8")
        content = base64.b64decode(blob)

        # Remove them from the list of students.
        students = [s for s in students if s not in repo_users]

        name = "_".join(repo_users) + ".ipynb"
        with open(out_dir / name, "wb") as f:
            f.write(content)
        print(f"{name} ({repo.html_url})")

    if len(students) != 0:
        print("\nNo notebook found for:")
        print("\n".join(students))

    print("\nFinished!")

if __name__ == "__main__":
    #main()
    fork()
