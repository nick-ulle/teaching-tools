"""This module contains functions for working with Jupyter notebooks.
"""
from pathlib import Path
import re

import nbformat as nb

RUBRIC_CELL_TEMPLATE = (
    '<strong style="color:#F00">Rubric Grade</strong>\n'
    '\n'
    'Category | Score\n'
    '-------- | -----\n'
    'R1 |\n'
    'R2 |\n'
    'F1 |\n'
    'F2 |\n'
    'C1 |\n'
    'C2 |\n'
    '\n'
    'Notes:\n'
)
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


def init_rubric(path, in_glob = "hw*.ipynb", out_name = "feedback.ipynb"):
    """Create a feedback file in a directory that already contains a notebook.
    """
    # Copy assignment notebook.
    path = Path(path)
    notebooks = list(path.glob(in_glob))
    if len(notebooks) < 1:
        print("Missing notebook for '{}'".format(path.name))

    notebook = nb.read(str(notebooks[0]), 4)

    text = RUBRIC_CELL_TEMPLATE
    cell = nb.v4.new_markdown_cell(text)
    cell["metadata"]["tags"] = ["grade"]
    notebook["cells"].insert(0, cell)

    nb.validate(notebook)
    nb.write(notebook, str(path / out_name))


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
                try:
                    grade_cell = new_grade_cell(cell)
                    cells.insert(j, grade_cell)
                except AttributeError as e:
                    pass

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


def compute_grade(path):
    path = Path(path)
    notebook = nb.read(str(path / "feedback.ipynb"), 4)

    # For rubric grading, the first 'grade' cell is the only one.
    grade_cell = next(
            cell for cell in notebook.cells
            if "tags" in cell["metadata"] and
            "grade" in cell["metadata"]["tags"]
    )

    # Find the table in the grade cell.
    lines = grade_cell["source"].split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("R1"))
    end = next(i for i, l in enumerate(lines) if l.startswith("C2"))
    lines = lines[start:(end + 1)]

    # Extract the scores from the table.
    scores = (l.split("|")[-1].strip() for l in lines)
    try:
        score = sum(float(s) for s in scores)
    except ValueError:
        print("Could not grade '{}'.".format(path))
        score = None

    return (path.name, score)

