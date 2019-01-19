#!/usr/bin/env python3
"""Grade Cell Cleaner

This script can remove all grade cells from a Jupyter notebook.
"""

import nbformat as nb
import os

IN_PATH = 'hw2/grades/'
GRADE_HEADER = "<span style='color:red'>Grade:",

paths = [
    os.path.join(IN_PATH, x) for x in os.listdir(IN_PATH)
    if x.endswith(".ipynb")
]

print("Converting files...")
for path in paths:
    notebook = nb.read(path, 4)
    notebook['cells'] = [
        cell for cell in notebook['cells']
        if not cell['source'].startswith(GRADE_HEADER)
    ]

    # Fix problem with Exercise 2.1 cell being merged.
    ex_header = '__Exercise 2.1.__'
    for i, cell in enumerate(notebook['cells']):
        if cell['source'].startswith('If we let'):
            sources = cell['source'].split(ex_header)
            if len(sources) != 2:
                continue

            # Split the cell.
            cell['source'] = sources[0]
            new_cell = nb.v4.new_markdown_cell(ex_header + sources[1])
            notebook['cells'].insert(i + 1, new_cell)

            break

    nb.write(notebook, path)
    print(path)

print("All done!")


