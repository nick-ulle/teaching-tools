#!/usr/bin/env python3
"""This module clones all of the student repositories for a given assignment.

To use this as a script, run

    python clone_hw.py NAME OUT

where NAME is the assignment name and OUT is the directory to clone into.
"""
import datetime as dt
from pathlib import Path
import sys

import pandas as pd
import pytz

import ucdtools.git as git
import ucdtools.notebook as note

SSH_URL = "git@github.com:2019-winter-ucdavis-sta141b/"
HTTPS_URL = "https://github.com/2019-winter-ucdavis-sta141b/"
GITHUB_LINK_PATH = "gh_link.csv"
DEADLINE = dt.datetime(
        2019, month = 1, day = 18, hour = 2, minute = 0,
        tzinfo = pytz.timezone("US/Pacific"))


def main():
    if len(sys.argv) != 3:
        print("Usage: python clone_hw.py NAME OUT")
        return

    name, path = sys.argv

    roster = pd.read_csv(GITHUB_LINK_PATH)

    cred = git.get_credentials(use_ssh = False)

    # Main loop
    print("Cloning repositories...")
    for user in roster.github:
        # Switch to SSH_URL for SSH
        url = "{}/{}-{}.git".format(HTTPS_URL, name, user)
        repo = git.clone_or_discover_repo(url, path, cred)

        git.check_late(repo, DEADLINE)

        note.init_feedback(Path(repo.path).parent)


if __name__ == "__main__":
    main()
