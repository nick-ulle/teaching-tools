"""This module is the configuration file for the grading tools.
"""

# Base URL to git repos. Pick one of HTTPS or SSH.
base_url = "https://github.com/2019-winter-ucdavis-sta141b/"
#base_url = "git@github.com:2019-winter-ucdavis-sta141b/"

# Path to CSV file that contains student emails and GitHub usernames.
users = "users.csv"


# ------------------------------------------------------------
# Time settings. DO NOT EDIT unless you know what you're doing.
from datetime import datetime
import pytz

year = datetime.now().year
tzinfo = pytz.timezone("US/Pacific")
