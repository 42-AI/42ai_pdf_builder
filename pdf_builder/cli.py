#!/usr/bin/env python3

# ============================================================================#
# =============================== LIBRARIES ==================================#
# ============================================================================#

import sys
import click
from pdf_builder.simple.checker import check_project_title, check_input_dir_simple
from pdf_builder.simple.copy import project_files_cpy
from pdf_builder.common.copy import cpy_template_file_to
from pdf_builder.common.utils import sub_run
from pdf_builder.common.format import insert_project_title, change_img_format,\
                                      file_add_clearpage, change_header_format,\
                                      set_url_color, change_equations_format,\
                                      change_empty_code_block_style, change_list_format
from pdf_builder.common.pandoc import run_pandoc, run_pandoc_all
from pdf_builder.bootcamp.checker import check_bootcamp_title, check_day_title, check_input_dir_bootcamp
from pdf_builder.bootcamp.copy import bootcamp_files_cpy
from pdf_builder.bootcamp.format import insert_day_title

# ============================================================================#
# ================================ FUNCTIONS =================================#
# ============================================================================#

@click.group()
def cli():
    pass

@click.command()
@click.option('--output-path',     '-o', help="Path to save the pdf to",                    required=True)
@click.option('--input-directory', '-d', help="Input directory of the project",             required=True, type=click.Path(exists=True))
@click.option('--project-title',   '-t', help="Title of the project",                       required=True)
@click.option('--logo-file',             help="Logo image file to use for the project",     default="templates/logo-42-ai.png")
@click.option('--template-file',         help="Latex Template file to use for the project", default="templates/template.latex")
@click.option('--debug',                 help="Logo image file to use for the project")
def simple(output_path, input_directory, project_title, logo_file, template_file, debug):
    
    try:
        check_project_title(project_title)
        check_input_dir_simple(input_directory)
        project_files_cpy(input_directory, template_file)
    except Exception as e:
        print(e)
        sys.exit(-1)
    
    # FILES FORMATTING
    #####################
    try:
        insert_project_title(project_title)
        files = sub_run("ls tmp/*.md").stdout.strip()
        for f in files.decode().split('\n'):
            content = None
            file_add_clearpage(f)
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
            if debug:
                run_pandoc(f)
        # GENERATING PDF OUTPUT
        run_pandoc_all(
            output_path.split('/')[-1], debug)
        print("Successfully built pdf !")
    except Exception as e:
        print(e)
        sys.exit(-1)

@click.command()
@click.option('--output-path',     '-o', help="Path to save the pdf to",                    required=True)
@click.option('--input-directory', '-d', help="Input directory of the project",             required=True, type=click.Path(exists=True))
@click.option('--bootcamp-title',  '-b', help="Title of the bootcamp",                      required=True)
@click.option('--day-title',       '-t', help="Title of the day",                           required=True)
@click.option('--logo-file',             help="Logo image file to use for the project",     default="templates/logo-42-ai.png")
@click.option('--template-file',         help="Latex Template file to use for the project", default="templates/template.latex")
@click.option('--debug',                 help="Logo image file to use for the project")
def bootcamp(output_path, input_directory, bootcamp_title, day_title, logo_file, template_file, debug):
    
    try:
        check_bootcamp_title(bootcamp_title)
        check_day_title(day_title)
        check_input_dir_bootcamp(input_directory)
        bootcamp_files_cpy(input_directory, template_file)
    except Exception as e:
        print(e)
        sys.exit(-1)
    
    # FILES FORMATTING
    #####################
    try:
        insert_project_title(bootcamp_title)
        insert_day_title(day_title)
        files = sub_run("ls tmp/*.md").stdout.strip()
        for f in files.decode().split('\n'):
            content = None
            file_add_clearpage(f)
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
            if debug:
                run_pandoc(f)
        # GENERATING PDF OUTPUT
        run_pandoc_all(
            output_path.split('/')[-1], debug)
        print("Successfully built pdf !")
    except Exception as e:
        print(e)
        sys.exit(-1)

cli.add_command(simple)
cli.add_command(bootcamp)