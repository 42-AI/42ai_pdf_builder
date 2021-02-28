#!/usr/bin/env python3

# ============================================================================#
# =============================== LIBRARIES ==================================#
# ============================================================================#

from pdf_builder.common.utils import sub_run, error

# ============================================================================#
# ================================ FUNCTIONS =================================#
# ============================================================================#


# RUN PANDOC
###############


def run_pandoc(file_name):
    """
    Build pdf file for each markdown.

    Args:
        file_name (undefined):

    """
    res = sub_run("pandoc {} --to=pdf --pdf-engine=pdflatex --highlight-style=breezedark\
     -t latex -o {} --template=tmp/template.latex"
                  .format(file_name, file_name + ".pdf"))
    if res.stderr:
        print(file_name)
        error(res.stderr.decode().strip(), file_name)


def run_pandoc_all(outfile, debug):
    """
    Build a pdf with all markdown files.

    Args:
        outfile (undefined): output file name
        debug (undefined): debug option

    """
    res = sub_run("pandoc tmp/*.md --to=pdf --pdf-engine=pdflatex --highlight-style=breezedark\
     -t latex -o {} --template=tmp/template.latex".format(outfile))
    if res.stderr:
        error(res.stderr.decode().strip())
    if not debug:
        sub_run("rm -rf tmp")