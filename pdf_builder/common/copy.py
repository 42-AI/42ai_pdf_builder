#!/usr/bin/env python3

# ============================================================================#
# =============================== LIBRARIES ==================================#
# ============================================================================#

import re
import pkg_resources
from pdf_builder.common.utils import sub_run

# ============================================================================#
# ================================ FUNCTIONS =================================#
# ============================================================================#


def cpy_template_file_to(source, destination):
    stream = pkg_resources.resource_stream(__name__, '../' + source) 
    with open(destination, 'wb') as _out:
        _out.write(stream.read())


def project_files_cpy(input_dir, template_file):
    """
    Copy project files and create a temporary directory.
    Args:
        input_dir (undefined): input day directory
        template_file (undefined): template file
    """
    # retrieve file lists
    project_f = sub_run("ls {0}/project*.md".format(input_dir)).stdout.strip()
    ex_list = sub_run("ls {}/**/ex*.md".format(input_dir)).stdout
    imgs_dir = sub_run("ls -d {}/assets".format(input_dir))

    # create a tmp dir with a copy of all files
    sub_run("rm -rf tmp")
    sub_run("mkdir -p tmp")
    if not imgs_dir.stderr:
        sub_run("cp -rp {} tmp/".format(imgs_dir.stdout.decode().strip()))
    sub_run("cp {} tmp/day.md".format(project_f.decode()))
    cpy_template_file_to('templates/logo-42-ai.png', 'tmp/logo-42-ai.png')
    cpy_template_file_to('templates/template.latex', 'tmp/template.latex')

    for f in ex_list.split():
        pattern = re.compile(r'(ex[0-9]{2}\.md)$')
        for e in pattern.findall(f.decode()):
            sub_run("cp {} tmp/{}".format(f.decode(),  e[:-3] + "_master.md"))
        pattern = re.compile(r'(ex[0-9]{2}_interlude.*)$')
        for e in pattern.findall(f.decode()):
            sub_run("cp {} tmp/".format(f.decode()))