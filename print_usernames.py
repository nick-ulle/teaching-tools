#!/usr/bin/env python3
"""This module merges a GitHub Classroom roster and Google Form and UC Davis
Photo Roster, all by email. Students missing a GitHub username are then
printed.

If this script is run with an argument, the argument is used as a path to save
a CSV of all enrolled students with a known GitHub username.
"""
import pandas as pd
import sys

import ucdtools.roster as rt


def read_google_form(path, ignore = rt.IGNORE_EMAILS):
    """Read a CSV from a Google Form that collects GitHub usernames.
    """
    form = pd.read_csv(path)

    form.columns = ("time", "email", "github", "group")

    return form[~form["email"].isin(ignore)]


def merge_by_email(gh, hw, ro):
    """This function returns a data frame with each student's email, GitHub
    Classroom username, and self-reported username.
    """
    m = gh.merge(hw, on = "email", how = "outer", suffixes = ("_gh", "_hw"))

    m = m.merge(ro, on = "email", how = "outer", suffixes = ("", "_ro"))

    return m


def main():
    m = merge_by_email(
            rt.read_github("classroom_roster.csv")
            , read_google_form("hw1_form.csv")
            , rt.read_ucd("roster_0220.xls")
    )

    # Print out all rows where 
    is_mismatched = m.github_gh != m.github_hw
    is_na = m.github_gh.isna() | m.github_hw.isna()

    cols = ("first_name", "last_name", "email", "github_gh", "github_hw")

    print("Mismatched usernames:\n")
    ans = m.loc[is_mismatched | is_na, cols]
    ans.sort_values(["last_name", "first_name"], inplace = True)
    print(ans)
 
    if len(sys.argv) <= 1:
        return

    path = sys.argv[1]
    print(f"\nWriting usernames for enrolled students to '{path}'")

    cols = ["email", "github_gh", "id"]
    ans = m.loc[~m.last_name.isna() & ~m.github_gh.isna(), cols]
    ans.columns = cols
    ans.to_csv(path, index = False)


if __name__ == "__main__":
    main()
