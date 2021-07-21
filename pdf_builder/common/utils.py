#!/usr/bin/env python3

# ============================================================================#
# =============================== LIBRARIES ==================================#
# ============================================================================#

import sys
import subprocess

# ============================================================================#
# ================================ FUNCTIONS =================================#
# ============================================================================#


def error(s, Warn=False, infile=None, line_nb=-1):
    """
    Raises error or warning at file/line precision.
    Args:
        s (undefined)           : error message
        Warn=False (undefined)  : Warn flag (true if warning, else error)
        infile=None (undefined) : file name
        line_nb=-1 (undefined)  : line number
    """
    out = "[Error]" if not Warn else "[Warning]"
    out += " {}".format(infile) if infile else ""
    out += ":{}".format(line_nb + 1) if line_nb > -1 else ""

    if not Warn:
        raise Exception("{} :: {}".format(out, s))
    print("{} : {}".format(out, s))


def sub_decorator(func):
    """
    Decorator to run command lines, catch exceptions.
    Args:
        func (undefined):
    Decorator for subprocess run (try catch errors)
    """
    def wrapper_func(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return (res)
        except Exception as e:
            print("{} Exception Detected!\n{}".format(*args, e))
            sys.exit(-1)

    return wrapper_func


@sub_decorator
def sub_run(command):
    """
    Run a bash command and show output/error.
    Args:
        command (undefined): command line
    """
    out = subprocess.run(command,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    return (out)
