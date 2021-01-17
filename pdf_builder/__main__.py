#!/usr/bin/env python3

# ============================================================================#
# =============================== LIBRAIRIES =================================#
# ============================================================================#

import argparse
import sys

from files_formatting import \
    day_files_cpy,\
    input_file_cpy,\
    insert_bootcamp_title,\
    insert_day_title,\
    files_format,\
    change_list_format,\
    change_header_format,\
    change_equations_format,\
    change_empty_code_block_style,\
    change_img_format,\
    set_url_color,\
    run_pandoc,\
    run_pandoc_all
from params_check import \
    check_bootcamp_title,\
    check_day_title,\
    check_input_dir,\
    check_input_file
from utils import sub_run


# ============================================================================#
# ================================ FUNCTIONS =================================#
# ============================================================================#


def get_arguments():
    """
        Get the program arguments.
            --bootcamp_title   :: title of the bootcamp
            --day_title        :: title of the day
            --output_file      :: pdf output name (ex: day00.pdf)
            --input_dir        :: input directory for the day
            --input_file       :: if only a file is given this can be used
                                    (for documentation)
            --template_file    :: template file used to generate the pdf
            --debug            :: debug option (in case of error)
    """

    parser = argparse.ArgumentParser(description='A pdf builder for 42-AI \
        projects')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-b', '--bootcamp_title', type=str, help='title of\
        the bootcamp (ex: "Machine Learning")', required=True)
    parser.add_argument('-t', '--day_title', type=str, default="Day00 - \
        PostgreSQL",
                        help='Title of the day (or documentation)',
                        required=True)
    parser.add_argument('-o', '--output_file', type=str, help='Pdf output\
         file (ex: "day00.pdf")', required=True)
    group.add_argument('-d', '--input_dir', type=str,
                       help='Directory of the day (ex:\
                              "bootcamp_python/day00"')
    group.add_argument('-f', '--input_file', type=str,
                       help='Specific markdown file (for documentation)')
    parser.add_argument('--template_file', type=str,
                        default="assets/template.latex",
                        help='latex template file for building pdfs')
    parser.add_argument('-w', '--debug', action='store_true',
                        help='debug option (builds each markdown \
                            independently)')
    args = parser.parse_args()
    return (args)


# ============================================================================#
# =================================== MAIN ===================================#
# ============================================================================#

def main():
    args = get_arguments()

    # CHECK PARAMETERS AND FILES
    ###############################
    try:
        check_bootcamp_title(args.bootcamp_title)
        check_day_title(args.day_title)

        if args.input_dir:  # check and copy the day directory
            check_input_dir(args.input_dir)
            day_files_cpy(args.input_dir, args.template_file)
        else:               # check and copy the documentation file
            check_input_file(args.input_file)
            input_file_cpy(args.input_file, args.template_file)
    except Exception as e:
        print(e)
        sys.exit(-1)

    # FILES FORMATTING
    #####################
    try:
        insert_bootcamp_title(args)
        insert_day_title(args)
        files = sub_run("ls tmp/*.md").stdout.strip()
        for f in files.decode().split('\n'):
            content = None
            files_format(f)
            with open(f, 'r') as infile:
                content = infile.read()
                content = change_img_format(f, content)
                content = change_header_format(f, content)
                content = change_list_format(f, content)
                content = change_empty_code_block_style(
                    f, content)
                content = change_equations_format(f, content)
                content = set_url_color(f, content)
            with open(f + ".tmp", 'w') as outfile:
                outfile.write(content)
            sub_run("mv {0}.tmp {0}".format(f))
            if args.debug:
                run_pandoc(f)
        # GENERATING PDF OUTPUT
        run_pandoc_all(
            args.output_file.split('/')[-1], args.debug)
        print("Successfully built pdf !")
    except Exception as e:
        print(e)
        sys.exit(-1)


if __name__ == "__main__":
    main()
