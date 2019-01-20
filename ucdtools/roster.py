"""This module contains functions for reading rosters into neatly-formatted
Pandas data frames.
"""
import pandas as pd


IGNORE_EMAILS = ["naulle@ucdavis.edu", "xidwang@ucdavis.edu",
        "shjiang@ucdavis.edu", "boxli@ucdavis.edu"]
ROSTER_SKIPROWS = 8


def read_github_roster(path, ignore = IGNORE_EMAILS):
    """Read a CSV roster from GitHub Classroom.
    """
    gh = pd.read_csv(path)

    gh.columns = ("email", "github", "github_id", "name")

    # Remove the ignored emails.
    return gh[~gh["email"].isin(ignore)]


def read_roster(path, ignore = IGNORE_EMAILS):
    """Read an XLS roster from UC Davis Photo Rosters.
    """
    roster = pd.read_excel(path, skiprows = ROSTER_SKIPROWS)

    roster.columns = ("id", "last_name", "first_name", "status", "section",
            "email", "level", "class")

    # Remove the ignored emails.
    return roster[~roster["email"].isin(ignore)]

def split_emails(emails):
    return (e.split("@")[0] for e in emails)
