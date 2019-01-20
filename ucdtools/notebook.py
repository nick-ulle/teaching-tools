"""This module contains functions for working with Jupyter notebooks.
"""
from pathlib import Path
import re

import nbformat as nb

GRADE_CELL_TEMPLATE = (
    '<span style="color:#F00">'
    'Exercise {} Grade<br />\n'
    '/{}\n'
    '</strong>\n\n'
    'Notes:\n'
)
EXERCISE_PATTERN = re.compile(
        r"__Exercise ([0-9]\.[0-9]{1,3}) \(([0-9]+) points\)\.?__"
)


def init_feedback(path, in_glob = "hw*.ipynb", out_name = "feedback.ipynb"):
    """Create a feedback file in a directory that already contains a notebook.
    """
    # Copy assignment notebook.
    path = Path(path)
    notebooks = list(path.glob(in_glob))
    if len(notebooks) < 1:
        print("Missing notebook for '{}'".format(path.name))

    notebook = nb.read(str(notebooks[0]), 4)

    insert_grade_cells(notebook)

    nb.validate(notebook)
    nb.write(notebook, str(path / out_name))


def has_tag(tag, cell):
    metadata = cell["metadata"]
    return "tags" in metadata and tag in metadata["tags"]


def insert_grade_cells(notebook):
    i = 0
    cells = notebook["cells"]

    while i < len(cells):
        cell = cells[i]

        if has_tag("exercise", cell):
            # Exercise Cell
            j = i + 1
            if j < len(cells) and has_tag("grade", cells[j]):
                # Already has a grade cell, so do nothing.
                pass
            else:
                # Insert a new grade cell.
                grade_cell = new_grade_cell(cell)
                cells.insert(j, grade_cell)

            i += 2

        else:
            i += 1


def new_grade_cell(exercise):
    """Create a grade cell for an exercise cell."""
    m = EXERCISE_PATTERN.search(exercise["source"])
    ex = m.group(1)
    points = m.group(2)

    text = GRADE_CELL_TEMPLATE.format(ex, points)

    cell = nb.v4.new_markdown_cell(text)
    cell["metadata"]["tags"] = ["grade"]

    return cell



