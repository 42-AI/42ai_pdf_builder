# ============================================================================#
# =============================== LIBRAIRIES =================================#
# ============================================================================#

import os
import re

from utils import error, sub_run


# ============================================================================#
# ================================ FUNCTIONS =================================#
# ============================================================================#


def check_bootcamp_title(title: str):
    """
    Check the format of bootcamp title

    Args:
        title (str): bootcamp title
    """
    if not title or len(title) < 3 or len(title) > 30:
        error("invalid bootcamp title length ! (length must be between \
3 and 30)")
    if re.search(r'[^a-zA-Z\s:]', title):
        error("invalid bootcamp title chars ([A-Za-z ] allowed)")
    return (True)


def check_input_dir(directory: str):
    """
    Check the bootcamp directory file organization

    Args:
        directory (str): bootcamp day directory
    """
    # check directory is in the format dayXX
    while directory[-1] == '/':
        directory = directory[:-1]
    dir = directory.split('/')[-1]
    day_regex = re.compile(r'^day[0-9]{2}$')
    module_regex = re.compile(r'^module[0-9]{2}$')
    if not day_regex.search(dir) and not module_regex.search(dir):
        error("'{}' invalid day/module directory (dayXX/moduleXX allowed)".format(directory))

    # check if it is a directory
    if not os.path.isdir(directory):
        error("'{}' is not a directory !".format(directory))

    # check directory has a dayXX.md
    ls_day = sub_run("ls {}/day*.md".format(directory))
    ls_module = sub_run("ls {}/module*.md".format(directory))

    if ls_day.stderr and ls_module.stderr:
        error("markdown for day/module missing")

    # check directory has exXX.md files
    ls_ex = sub_run("ls {}/ex*/ex*.md".format(directory))
    if ls_ex.stderr:
        error("markdown for exercices missing")


def check_input_file(input_file: str):
    """
    Check if file exists and is markdown.

    Args:
        input_file (str): file name

    """
    if not os.path.isfile(input_file):
        error("'{}' is not a file !".format(input_file))
    if input_file.split('.')[-1] != "md":
        error("'{}' is not a markdown file".format(input_file))


def check_day_title(title: str):
    """
    Check the day title format.

    Args:
        title (str): title

    """
    if not title or len(title) < 14 or len(title) > 40:
        error("invalid day/module title length ! (length must be between\
 11 and 40)")
    if re.search(r'[^A-Za-z\d -]', title):
        error("invalid day/module title chars ([A-Za-z -] allowed)")
    if re.search(r'^(?!Day[0-9]{2} - ).*', title) and re.search(r'^(?!Module[0-9]{2} - ).*', title):
        error("invalid day/module title format (it must be formatted as follows\
             \"DayXX - ...\")")
    return (True)
