#!/usr/bin/env python3
"""Assignment Notebook Tool

This script can strip solution cells or insert grading cells in Jupyter
notebooks.
"""

import argparse
import glob
import nbformat as nb
import os.path


# Configuration Variables
SOLN_SUFFIX = '-solutions.ipynb'
SOLN_HEADER = '#### SOLUTION' # header for solution cells

EXERCISE_POINTS = {
      '1.1': 20, '1.2': 40, '1.3': 10, '1.4': 10
    , '2.1': 20, '2.2': 10
    , '3.1': 20, '3.2': 10
}


def nb_strip(args):
    """Remove solution cells from notebooks."""
    path = args.source

    if not path.endswith(SOLN_SUFFIX):
        msg = "Error: input path '{}' doesn't end with '{}'."
        print(msg.format(path, SOLN_SUFFIX))
        return

    out_path = path[:-len(SOLN_SUFFIX)] + '.ipynb'
    if os.path.exists(out_path):
        print("Error: output path '{}' already exists.".format(out_path))
        return 

    # Strip solution cells.
    notebook = nb.read(path, nb.NO_CONVERT)
    notebook['cells'] = [
        cell for cell in notebook['cells']
        if not cell['source'].startswith(SOLN_HEADER)
    ]

    # Write the stripped notebook to a file.
    nb.write(notebook, out_path)
    print("Wrote '{}'.".format(out_path))


def nb_grade(args):
    """Add grade cells to notebooks."""
    # Check the source and target paths.
    source = os.path.join(args.source, "*.ipynb")
    paths = glob.glob(source)
    if len(paths) == 0:
        print(f"Error: invalid input path '{source}'.")
        return None

    if not os.path.isdir(args.target):
        try:
            os.mkdir(args.target)
        except:
            print(f"Error: invalid output path '{args.target}'.")
            return None

    # Convert the notebooks.
    for path in paths:
        target = os.path.join(args.target, os.path.basename(path))
        print(f"'{path} -> {target}'")

        notebook = nb.read(path, 4)

        # Insert a grade cell before every exercise cell.
        i = 0
        cells = notebook['cells']
        while i < len(cells):
            cell = cells[i]
            # In newer assignment notebooks we can check metadata instead.
            if cell['source'].startswith('__Exercise'):
                # Exercise cell: insert a new grade cell before.
                grade_cell = create_grade_cell(cell)
                cells.insert(i, grade_cell)
                i += 2
            elif cell['metadata'].get('name', '').startswith('gr'):
                # Grade cell: skip past the subsequent exercise cell.
                i += 2
            else:
                i += 1

        nb.validate(notebook)
        nb.write(notebook, target)


def create_grade_cell(cell):
    """Create a grade cell for an exercise cell."""
    header = cell['source'].split('__')[1]
    ex_number = header.strip('_.').split(' ')[-1]

    points = EXERCISE_POINTS[ex_number]
    text = (
        '<strong style="color:#F00">\n'
        f'Grade: /{points}\n\n'
        'Notes:\n'
        '</strong>'
    )

    grade_cell = nb.v4.new_markdown_cell(text)
    grade_cell['metadata']['name'] = f'gr{ex_number}'

    return grade_cell


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(help = 'action to take')

    # Strip Tool Arguments ----------------------------------------
    p_strip = sp.add_parser('strip')
    p_strip.add_argument('source', help = 'path to input file')
    p_strip.set_defaults(subprogram = nb_strip)

    # Grade Tool Arguments ----------------------------------------
    p_grade = sp.add_parser('grade')
    p_grade.add_argument('source', help = 'path to input directory')
    p_grade.add_argument('target', help = 'path to output directory')
    p_grade.set_defaults(subprogram = nb_grade)

    # Parse arguments and run subprogram
    args = ap.parse_args()
    args.subprogram(args)


if __name__ == '__main__':
    main()
