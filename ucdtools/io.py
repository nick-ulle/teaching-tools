"""This module contains functions for reading and writing student information
from Canvas, UC Davis Photo Rosters, Piazza, and GitHub Classroom.
"""
import pandas as pd


IGNORE_EMAILS = ["naulle@ucdavis.edu", "xidwang@ucdavis.edu",
        "shjiang@ucdavis.edu", "boxli@ucdavis.edu", "dtemplelang@ucdavis.edu"]
ROSTER_SKIPROWS = 8

# Columns required for Canvas grade import.
CANVAS_COLS = ["Student", "ID", "SIS User ID", "SIS Login ID", "Section"]


def split_emails(emails):
    return (e.split("@")[0] for e in emails)


def read_github(path, ignore = IGNORE_EMAILS):
    """Read a CSV roster from GitHub Classroom.
    """
    gh = pd.read_csv(path)

    gh.columns = ("email", "github", "github_id", "name")

    # Remove the ignored emails.
    return gh[~gh["email"].isin(ignore)]


def read_ucd(path, ignore = IGNORE_EMAILS):
    """Read an XLS roster from UC Davis Photo Rosters.
    """
    roster = pd.read_excel(path, skiprows = ROSTER_SKIPROWS,
            dtype = {0: str})

    roster.columns = ("id", "last_name", "first_name", "status", "section",
            "email", "level", "class")

    # Remove the ignored emails.
    return roster[~roster["email"].isin(ignore)]


def read_piazza(path, ignore = IGNORE_EMAILS):
    """Read a CSV statistics file from Piazza.
    """
    df = pd.read_csv(path)

    return df[~df["email"].isin(ignore)]


def read_canvas(path):
    """Read a CSV gradebook file from Canvas.
    """
    df = pd.read_csv(path, dtype = {"ID": str, "SIS User ID": str})

    return df


def write_canvas(path, canvas, col):
    """Write a data frame to Canvas gradebook format.
    """
    canvas[CANVAS_COLS + [col]].to_csv(path, index = False)


def read_students(path):
    """Read a students file from the merge_students script.
    """
    df = pd.read_csv(path, dtype = {"ID": str, "SIS User ID": str})

    return df
