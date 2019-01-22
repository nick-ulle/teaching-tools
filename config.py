"""This module is the configuration file for the grading tools.
"""
from datetime import datetime

import pytz

# Base URL to git repos. Pick HTTPS or SSH.
base_url = "https://github.com/2019-winter-ucdavis-sta141b/"
#base_url = "git@github.com:2019-winter-ucdavis-sta141b/"

year = datetime.now().year
tzinfo = pytz.timezone("US/Pacific")
