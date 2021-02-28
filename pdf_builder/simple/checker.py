#!/usr/bin/env python3

# ============================================================================#
# =============================== LIBRARIES ==================================#
# ============================================================================#

import os
import re
from pdf_builder.common.utils import error, sub_run

# ============================================================================#
# ================================ FUNCTIONS =================================#
# ============================================================================#

def check_project_title(title: str):
    """
    Check the format of project title
    Args:
        title (str): project title
    """
    if not title or len(title) < 3 or len(title) > 30:
        error("invalid project title length ! (length must be between \
3 and 30)")
    if re.search(r'[^a-zA-Z\s:]', title):
        error("invalid project title chars ([A-Za-z ] allowed)")
    return (True)


def check_input_dir_simple(directory: str):
    """
    Check the bootcamp directory file organization
    Args:
        directory (str): bootcamp day directory
    """
    # check directory is in the format dayXX
    while directory[-1] == '/':
        directory = directory[:-1]
    
    # check if it is a directory
    if not os.path.isdir(directory):
        error("'{}' is not a directory !".format(directory))

    # check directory has a projectXX.md
    ls_project = sub_run("ls {}/project*.md".format(directory))

    if ls_project.stderr:
        error("markdown for project missing")

    # check directory has exXX.md files
    ls_ex = sub_run("ls {}/ex*/ex*.md".format(directory))
    if ls_ex.stderr:
        error("markdown for exercises missing")