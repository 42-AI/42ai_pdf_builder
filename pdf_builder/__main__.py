#!/usr/bin/env python3

#==============================================================================#
#=============================== LIBRAIRIES ===================================#
#==============================================================================#

import os
import sys
import argparse

from utils import logger, sub_run
import params_check
import files_formatting 

#==============================================================================#
#================================ FUNCTIONS ===================================#
#==============================================================================#


def get_arguments():
    parser = argparse.ArgumentParser(description='A pdf builder for 42-AI projects')
    parser.add_argument('-b', '--bootcamp_title', type=str, help='input rules file', required=True)
    parser.add_argument('-t', '--pdf_title', type=str, default="Day00 - PostgreSQL",
        help='Title of the day (can for documentation)', required=True)
    parser.add_argument('-o', '--output_file', type=str, help='Pdf output file', required=True)
    parser.add_argument('-d', '--input_dir', type=str, help='Directory of the day')
    parser.add_argument('-f', '--input_file', type=str,
        help='Specific markdown file (for documentation)')
    parser.add_argument('--template_file', type=str, default="assets/template.latex", help='template file')
    parser.add_argument('-w', '--debug', action='store_true', help='debug option (builds each markdown independently)')
    args = parser.parse_args()
    return(args)

#==============================================================================#
#=================================== MAIN =====================================#
#==============================================================================#

def main():
    args = get_arguments()

    try:
        params_check.check_bootcamp_title(args.bootcamp_title)
        params_check.check_day_title(args.pdf_title)
        params_check.check_file_dir(args)

        if args.input_dir:
            params_check.check_input_dir(args.input_dir)
            files_formatting.day_files_cpy(args.input_dir, args.template_file)
        else:
            params_check.check_input_file(args.input_file)
            files_formatting.input_file_cpy(args.input_file, args.template_file)
        
        files_formatting.insert_bootcamp_title(args)
        files_formatting.insert_day_title(args)

        
        files = sub_run("ls tmp/*.md").stdout.strip()
        for f in files.decode().split('\n'):
            logger.info("PROCESSING '{}' !".format(f))
            files_formatting.files_format(f)
            files_formatting.replace_blank_code_blocks(f)
            files_formatting.format_list(f)
            files_formatting.change_img_format(f)
            files_formatting.set_url_color(f)

            if args.w:
                files_formatting.run_pandoc(f)

        files_formatting.run_pandoc_all(args.output_file.split('/')[-1])
        logger.info("Successfully created '{}' !".format(os.getcwd() + "/" + args.output_file.split('/')[-1]))
    except Exception as e:
        print(e)
        sys.exit(-1)

if __name__ == "__main__":
    main()
