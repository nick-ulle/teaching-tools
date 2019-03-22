#!/usr/bin/env python3

import pandas as pd

import ucdtools.roster as io

CANVAS_PATH = "canvas_0322.csv"
ROSTER_PATH = "roster_0321.xls"
PIAZZA_PATH = "piazza_0321.csv"
GITHUB_PATH = "github_0322.csv"
OUTPUT_PATH = "students.csv"
PIAZZA_REMAP = dict()
    # canvas: piazza


def main():
    # Merge Canvas, Roster, and Piazza. Optionally GitHub.
    # Output students.csv.

    # ----------------------------------------
    # First merge Canvas to Roster so we have emails.
    canvas = io.read_canvas(CANVAS_PATH)
    canvas = canvas[["Student", "ID", "SIS User ID", "SIS Login ID",
        "Section"]]
    canvas = canvas[~canvas["SIS User ID"].isna()]

    roster = io.read_ucd(ROSTER_PATH)
    roster = roster[["id", "email", "last_name", "first_name"]]

    students = pd.merge(canvas, roster, "left",
            left_on = "SIS User ID", right_on = "id")
    students.drop("id", axis = 1)

    is_missing = students["email"].isna()
    if any(is_missing):
        print("No SIS ID match for:")
        print(students.loc[is_missing, ["Student", "SIS User ID"]], "\n")

    del canvas
    del roster

    # ----------------------------------------
    # Now match Piazza to the merged students.
    students["piazza"] = students["email"].replace(PIAZZA_REMAP)

    piazza = io.read_piazza(PIAZZA_PATH)
    piazza = piazza[["name", "email"]]

    unmatched = students[~students["piazza"].isin(piazza["email"])]
    if unmatched.shape[0] > 0:
        print("No Piazza email match for:")
        print(unmatched[["Student", "SIS User ID", "email"]], "\n")

        candidates = piazza[~piazza["email"].isin(students["piazza"])]

        print("Best candidates:")
        names = pd.concat([unmatched["last_name"], unmatched["first_name"]])
        pattern = "|".join(names)
        print(candidates[candidates["name"].str.contains(pattern)], "\n")

        print("All candidates:")
        print(candidates, "\n")

    del piazza

    # ----------------------------------------
    # Now match GitHub to the merged students.
    github = io.read_github(GITHUB_PATH)
    github = github[["email", "github"]]

    students = pd.merge(students, github, "left", on = "email")
    is_missing = students["github"].isna()
    if any(is_missing):
        print("No GitHub match for:")
        print(students.loc[is_missing, ["Student", "SIS User ID", "email"]],
                "\n")

    # ----------------------------------------
    # Finally, write out the CSV file.
    students.to_csv(OUTPUT_PATH, index = False)


if __name__ == "__main__":
    main()
