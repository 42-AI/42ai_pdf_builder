#!/usr/bin/env python3

# ============================================================================#
# =============================== LIBRARIES ==================================#
# ============================================================================#

import re

# ============================================================================#
# ================================ FUNCTIONS =================================#
# ============================================================================#


# INSERT BOOTCAMP TITLE / PDF TITLE
######################################

def get_line_containing(file, content):
    """
    Search a line containing a specific content.

    Args:
        file (undefined): file name
        content (undefined): searched content

    """
    index = 0
    with open(file, 'r') as infile:
        for idx, line in enumerate(infile):
            if re.match(r'.*{}.*'.format(content), line):
                index = idx + 1
    return (index)


def insert_line(file, idx, content):
    """
    Insert line into a file at a precise line.

    Args:
        file (undefined): file name
        idx (undefined): line number
        content (undefined): content to be added.

    """
    f = open(file, "r")
    contents = f.readlines()
    f.close()
    contents.insert(idx, "{}".format(content))
    f = open(file, "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()

def insert_day_title(day_title):
    """
    Insert day title to the template file.

    Args:
        args (undefined):

    """
    idx = get_line_containing("tmp/template.latex", "day_number")
    insert_line("tmp/template.latex", idx, day_title.split(' - ')[0])
    idx = get_line_containing("tmp/template.latex", "day_title")
    insert_line("tmp/template.latex", idx, day_title.split(' - ')[1])