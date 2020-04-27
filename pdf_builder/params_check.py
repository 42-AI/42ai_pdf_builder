#==============================================================================#
#=============================== LIBRAIRIES ===================================#
#==============================================================================#

import re
import os
#from pdf_builder import utils
from utils import error, sub_run, run_task

#==============================================================================#
#================================ FUNCTIONS ===================================#
#==============================================================================#


@run_task("Check bootcamp title")
def check_bootcamp_title(title:str):
    if not title or len(title) < 3:
        error("title too short (< 3 chars)")
    #check bootcamp title only has alpha char and space
    if not all(c.isalpha() or c.isspace() for c in title):
        error("invalid title chars ([A-Za-z ] allowed)")

    #check len of bootcamp title
    if not len(title) < 30:
        error("invalid title len (> 30 chars)")       


@run_task("Check input dir")
def check_input_dir(directory:str):
    #check directory is in the format dayXX
    while directory[-1] == '/':
        directory = directory[:-1]
    dir = directory.split('/')[-1]
    regex = re.compile(r'^day[0-9]{2}$')
    if not regex.search(dir):
        error("'{}' invalid day directory (dayXX allowed)".format(directory))

    #check if it is a directory
    if not os.path.isdir(directory):
        error("'{}' is not a directory !".format(directory))

    #check directory has a dayXX.md
    ls_day = sub_run("ls {}/day*.md".format(directory))
    if ls_day.stderr:
        error("markdown for day missing")

    #check directory has exXX.md files
    ls_ex = sub_run("ls {}/ex*/ex*.md".format(directory))
    if ls_ex.stderr:
        error("markdown for exercices missing")


@run_task("Check input file")
def check_input_file(input_file:str):
    if not os.path.isfile(input_file):
        error("'{}' is not a file !".format(input_file))
    if input_file.split('.')[-1] != "md":
         error("'{}' is not a markdown file".format(input_file))


@run_task("Check day title")
def check_day_title(title:str):
    regex = re.compile(r'^Day[0-9]{2} - .*')
    if not regex.search(title):
        error("'{}' invalid Day title (must be formatted as follows \"DayXX - ...\")".format(title))


@run_task("Check file or folder")
def check_file_dir(args):
    if args.input_dir and args.input_file:
        error("you provided a file AND a folder, please\
               provide a file OR a folder !")