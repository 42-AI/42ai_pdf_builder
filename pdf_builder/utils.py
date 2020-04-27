#!/usr/bin/env python3

##################
#   LIBRAIRIES   #
##################

import sys
import logging
import subprocess

OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(message)s",
                              "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

#################
#   FUNCTIONS   #
#################


def error(s):
    raise Exception("Error :: {}".format(s))


def run_task(desc=None, oneline=True):

    def run_task_decorator(func):
        task_desc = desc

        def wrapper_func(*args, **kwargs):
            if not oneline:
                logger.info("{} started.".format(task_desc.format(*args)))
            res = func(*args, **kwargs)
            logger.info("{} Done !".format(task_desc.format(*args)))
            return(res)
        return wrapper_func
    return run_task_decorator


def sub_decorator(func):
    def wrapper_func(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            logger.info(r"'{}' Done !".format(
                r'{}'.format("".join(*args).replace('\n', '\\n'))
            ))
            return(res)
        except Exception as e:
            logger.info("{} Exception Detected !\n{}".format(*args, e))
            sys.exit(-1)
    return wrapper_func


@sub_decorator
def sub_run(command):
    out = subprocess.run(command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    return (out)