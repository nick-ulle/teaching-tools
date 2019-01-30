# UC Davis Course Management Tools

This repository contains tools for managing courses at UC Davis. Most of these
tools arose from teaching the STA 141A-B-C series, and are written in R or
Python.

Name                  | Description
--------------------- | -----------

Programs include instructions for how to run them in the file.

## `ucdtool.py`

This script provides four subprograms to help manage student git repos:

*   `clone`: Clone multiple repo from a base URL.
*   `grade`: Create `feedback.ipynb` in every repo, based on the Jupyter
    notebook submitted by the student.
*   `commit`: Add and commit a user-specified file in every repo.
*   `push`: Push to `origin master` in every repo.

### Installation

The script requires four external packages:

Name     | Tested Version | Conda Install Command
-------- | -------------- | ---------------------
pandas   | 0.24.0         |
nbformat | 4.4.0          | `conda install -c anaconda nbformat`
pygit2   | 0.27.4         | `conda install -c conda-forge pygit2`
pytz     | 2018.7         | `conda install -c anaconda pytz`

If you don't use Anaconda, these packages can also be installed with `pip`.

Once you've installed the required packages, use `git clone` to clone this
repo.

### Usage

To use this tool to grade an assignment, the basic process is:

1.  Clone the assignments with `python ucdtool.py clone DEST NAME`. The `DEST`
    argument is the directory to clone the assignments into; it will be created
    if it doesn't exist already. The `NAME` argument is the name of the
    assignment on GitHub, for example "assignment-1". The name must match
    exactly.

2.  Generate a `feedback.ipynb` file in every repo with `python ucdtool.py
    grade PATH DUE`. The `PATH` argument is the directory that contains the
    assignment repos. The `DUE` argument is a due date in `MM.DD hh:mm` format.
    The due date is only used to print out the names of students that submitted
    late.

3.  Grade each `feedback.ipynb`, adding feedback directly in the notebook.
    Usually `feedback.ipynb` will have grading cells marked in red. However, if
    the student deleted parts of the original assignment notebook, these will
    not show up and you'll have to create grading cells manually.

4.  When all of the notebooks are graded, use `python ucdtool.py commit PATH
    FILE MESSAGE` to add and commit the graded notebooks. The `PATH` argument
    is the directory that contains the assignment repos. The `FILE` argument is
    the name of the file to add and commit, usually `feedback.ipynb`. The
    `MESSAGE` argument is the commit message.

5.  Finally, push with `python ucdtool.py push PATH`. The `PATH` argument is
    the directory that contains the assignment repos. **Be careful:** unlike
    steps 1-4, there is no "undo" for this step and students can immediately
    see the pushed commits.


## `print_usernames.py`

This script can merge rosters from GitHub Classroom and UC Davis Photorosters.
