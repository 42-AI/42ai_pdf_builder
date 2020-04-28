#!/usr/bin/env python3

#==============================================================================#
#=============================== LIBRAIRIES ===================================#
#==============================================================================#

import re
import platform
from utils import run_task, sub_run, error

#==============================================================================#
#================================ FUNCTIONS ===================================#
#==============================================================================#

# FILES COPY
###############


@run_task("Copying day files")
def day_files_cpy(input_dir, template_file):
    #retrieve file lists
    day_f = sub_run("ls {}/day*.md".format(input_dir)).stdout.strip()
    ex_list = sub_run("ls {}/**/ex*.md".format(input_dir)).stdout
    imgs_dir = sub_run("ls -d {}/assets".format(input_dir))

    #create a tmp dir with a copy of all files
    sub_run("rm -rf tmp")
    sub_run("mkdir -p tmp")
    if not imgs_dir.stderr:
        sub_run("cp -rp {} tmp/".format(imgs_dir.stdout.decode().strip()))
    sub_run("cp {} tmp/".format(day_f.decode()))
    sub_run("cp {} tmp/".format(day_f.decode()))
    sub_run("cp {} tmp/".format(template_file))
    for f in ex_list.split():
        pattern = re.compile(r'(ex[0-9]{2}\.md)$')
        for e in pattern.findall(f.decode()):
            #print(f.decode()[:-7]+ e[:-3] + "_master.md")
            sub_run("cp {} tmp/{}".format(f.decode(),  e[:-3] + "_master.md"))
        pattern = re.compile(r'(ex[0-9]{2}_interlude.*)$')
        for e in pattern.findall(f.decode()):
            sub_run("cp {} tmp/".format(f.decode()))
        #sub_run("cp {} tmp/".format(f.decode()))


@run_task("Copying input file")
def input_file_cpy(input_file, template_file):
    #create a tmp dir with a copy of all files
    sub_run("rm -rf tmp")
    sub_run("mkdir -p tmp")

    #copy input_file into tmp
    sub_run("cp {} tmp/".format(input_file))
    sub_run("cp {} tmp/".format(template_file))
    imgs_dir = sub_run("ls -d {}/assets".format("/".join(input_file.split('/')[:-1])))
    if not imgs_dir.stderr:
        sub_run("cp -rp {} tmp/".format(imgs_dir.stdout.decode().strip()))

# FILES FORMAT
#################


@run_task("Adding newpage")
def files_format(file_name):
    if platform.system() == "Darwin":
        sub_run("echo '\n\\\\clearpage' >> tmp/{}".format(file_name.split('/')[-1]))
    else:
        sub_run("echo '\n\\\\clearpage' >> tmp/{}".format(file_name.split('/')[-1]))

# IMAGE FORMAT
#################

@run_task("Changing images format")
def change_img_format(file_name):
    #pattern : ![_group1_](_group2_){_group3_}
    re_md = re.compile(r'\!\[(.*)\]\((.*)\)({.*})?')
    #pattern : <img src="_group1_ / _group2_" 
    re_html = re.compile(r'<img.*src=\"(.*\/(.*))\".*')

    with open(file_name+".tmp", 'w') as out_file:
        with open(file_name, 'r') as in_file:
            for l in in_file:
                if re_md.match(l):
                    groups = re_md.findall(l)[0]
                    caption = groups[0]
                    path = groups[1]
                    if len(groups) == 2:
                        width = "{{}}"
                    else:
                        width = groups[2]
                    #print(l.strip(), " => ", "![{}](tmp/assets/{})".format(caption, path.split('/')[-1]))
                    out_file.write("\n![{}](tmp/assets/{}){}\n".format(caption, path.split('/')[-1], width))
                elif re_html.match(l):
                    groups = re_html.findall(l)[0]
                    path = groups[0]
                    #print(l.strip(), " => ", "![{}](tmp/assets/{})".format("", path.split('/')[-1]))
                    out_file.write("\n![{}](tmp/assets/{})\n".format(path.split('/')[-1].split('.')[0], path.split('/')[-1]))
                else:
                    out_file.write(l)
    sub_run("mv {} {}".format(file_name+".tmp", file_name))

# INSERT BOOTCAMP TITLE / PDF TITLE
######################################


def get_line_containing(file, content):
    index = 0
    with open(file, 'r') as infile:
        for idx, line in enumerate(infile):
            if re.match(r'.*{}.*'.format(content), line):
                index = idx + 1
    return (index)


def insert_line(file, idx, content):
    f = open(file, "r")
    contents = f.readlines()
    f.close()
    contents.insert(idx, "{}".format(content))
    f = open(file, "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()


@run_task("Inserting bootcamp title")
def insert_bootcamp_title(args):
    idx = get_line_containing("tmp/template.latex", "bootcamp_title")
    insert_line("tmp/template.latex", idx,  args.bootcamp_title)


@run_task("Inserting day title")
def insert_day_title(args):
    idx = get_line_containing("tmp/template.latex", "day_number")
    insert_line("tmp/template.latex", idx, args.pdf_title.split(' - ')[0])
    idx = get_line_containing("tmp/template.latex", "day_title")
    insert_line("tmp/template.latex", idx, args.pdf_title.split(' - ')[1])

# CONVERT BLANK CODE BLOCKS TO BASH
######################################

@run_task("Replacing blank code blocks")
def replace_blank_code_blocks(file):
    idx = 0
    with open(file+".tmp", 'w') as outfile:
        with open(file, 'r') as infile:
            for l in infile:
                re_md = re.compile(r'^```.*')
                if re_md.match(l):
                    if idx % 2 == 0:
                        outfile.write("```bash\n")
                    else:
                        outfile.write(l)
                    idx += 1
                else:
                    outfile.write(l)
    sub_run("mv {0}.tmp {0}".format(file))

# DETECT LARGE CODE BLOCKS
#############################


@run_task("Detecting large code blocks")
def detect_large_blocks(file=None):
    if file:
        files = sub_run("ls tmp/*.md").stdout.strip()
    else:
        files = sub_run("ls tmp/ex*.md").stdout.strip()
    for f in files.decode().split('\n'):
        with open(f, 'r') as infile:
            pattern = re.compile(r'[\`]{3}[a-z]{1,10}.*?[\`]{3}' ,re.DOTALL)
            for match in pattern.findall(infile.read()):
                if match.count('\n') > 60:
                    error("'{}' file has '{}' lines in a code block (MAX LIMIT is 60)".format(f, match.count('\n')))


# FORMAT LIST
################

@run_task("Formating lists")
def format_list(file):
    with open("{}.tmp".format(file), "w") as outfile:
        with open(file, "r") as infile:
            for l in infile:
                if re.match(r'[*-]{1}[^*-]{1}', l):
                    outfile.write('\n')
                outfile.write(l)
    sub_run("mv {0}.tmp {0}".format(file))

# SET URL COLOR
##################


@run_task("Set url color")
def set_url_color(ifile=None):
    with open("{}.tmp".format(ifile), "w") as outfile:
        outfile.write("---\n")
        outfile.write("colorlinks: true\n")
        outfile.write("urlcolor: \"blue\"\n")
        outfile.write("---\n")
        with open(ifile, "r") as infile:
            for l in infile:
                outfile.write(l)
    sub_run("mv {0}.tmp {0}".format(ifile))

# RUN PANDOC
###############


@run_task("Pandoc build")
def run_pandoc(file_name):
    res = sub_run("pandoc {} --to=pdf --pdf-engine=pdflatex --highlight-style=breezedark\
     -t latex -o {} --template=tmp/template.latex".format(file_name, file_name + ".pdf"))
    if res.stderr:
        error(res.stderr.decode().strip())
    sub_run("rm {}".format(file_name + ".pdf"))

@run_task("PANDOC FINAL BUILD !")
def run_pandoc_all(outfile):
    res = sub_run("pandoc tmp/*.md --to=pdf --pdf-engine=pdflatex --highlight-style=breezedark\
     -t latex -o {} --template=tmp/template.latex".format(outfile))
    if res.stderr:
        error(res.stderr.decode().strip())
    sub_run("rm -rf tmp")