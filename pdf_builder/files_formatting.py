#!/usr/bin/env python3

# ============================================================================#
# =============================== LIBRAIRIES =================================#
# ============================================================================#

import re
import platform
from utils import sub_run, error

# ============================================================================#
# ================================ FUNCTIONS =================================#
# ============================================================================#

# FILES COPY
###############


def day_files_cpy(input_dir, template_file):
    """
    Copy files of a day and create a temporary directory.

    Args:
        input_dir (undefined): input day directory
        template_file (undefined): template file

    """
    # retrieve file lists
    day_f = sub_run("ls {}/day*.md".format(input_dir)).stdout.strip()
    ex_list = sub_run("ls {}/**/ex*.md".format(input_dir)).stdout
    imgs_dir = sub_run("ls -d {}/assets".format(input_dir))

    # create a tmp dir with a copy of all files
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
            sub_run("cp {} tmp/{}".format(f.decode(),  e[:-3] + "_master.md"))
        pattern = re.compile(r'(ex[0-9]{2}_interlude.*)$')
        for e in pattern.findall(f.decode()):
            sub_run("cp {} tmp/".format(f.decode()))


def input_file_cpy(input_file, template_file):
    """
    Copy input file and create tmp directory.

    Args:
        input_file (undefined): input file
        template_file (undefined): template file

    """
    # create a tmp dir with a copy of all files
    sub_run("rm -rf tmp")
    sub_run("mkdir -p tmp")

    # copy input_file into tmp
    sub_run("cp {} tmp/".format(input_file))
    sub_run("cp {} tmp/".format(template_file))
    imgs_dir = sub_run(
        "ls -d {}/assets".format("/".join(input_file.split('/')[:-1])))
    if not imgs_dir.stderr:
        sub_run("cp -rp {} tmp/".format(imgs_dir.stdout.decode().strip()))

# FILES FORMAT
#################


def files_format(file_name):
    """
    Add clearpages at the end of exercises.

    Args:
        file_name (undefined): file name

    """
    if platform.system() == "Darwin":
        sub_run(
            "echo '\n\\\\clearpage' >> tmp/{}"
            .format(file_name.split('/')[-1]))
    else:
        sub_run(
            "echo '\n\\\\clearpage' >> tmp/{}"
            .format(file_name.split('/')[-1]))

# IMAGE FORMAT
#################


def change_img_format(file_name: str, file_content: str):
    """
    Change the images format (also convert html images into markdown ones).

    Args:
        file_name (str): file name
        file_content (str): file content

    """
    groups = None
    title = None
    path = None
    style = None
    out = ""

    if len(file_content) == 0:
        error("empty file !", infile=file_name)

    img_pattern_md = re.compile(r'[\s]*\!\[(.*)\]\((.*)\)({.*})?')
    img_pattern_html = re.compile(r'[\s]*<img.*src=[\"\']{1}(.*)[\"\']{1}.*/>')
    for idx, line in enumerate(file_content.rstrip().split('\n')):
        if not img_pattern_md.match(line) and not img_pattern_html.match(line):
            out += line + "\n"
            continue

        if img_pattern_md.match(line):
            groups = img_pattern_md.findall(line)[0]
            title = groups[0]
            path = groups[1]
            style = groups[2]

        if img_pattern_html.match(line):
            groups = img_pattern_html.findall(line)[0]
            title = groups.split('/')[-1].split('.')[0]
            path = groups
            style = ''

        if len(title) == 0:
            error("empty image title !", Warn=True,
                  infile=file_name, line_nb=idx)
            title = path.split('/')[-1].split('.')[0]
        if len(path) == 0:
            error("empty image path !", infile=file_name, line_nb=idx)

        if len(style) != 0 and not re.match(r'.*width=[0-9]{1,4}px.*', style):
            error(
                "wrong image style format ! (example: '{width=250px}')",
                infile=file_name, line_nb=idx)

        path = "tmp/assets/" + path.split('/')[-1]
        out += "![{}]({}){}".format(title, path, style) + "\n"

    return (out)

# HEADER FORMAT
##################


def change_header_format(file_name: str, file_content: str):
    """
    Change and check the header format.

    Args:
        file_name (str): file name
        file_content (str): file content

    """
    out = ""

    if len(file_content) == 0:
        error("empty file !", infile=file_name)

    code_flag = 0
    header_pattern = re.compile(r'([\s]*)([#]{1,4})[\s]+(.*)')
    for idx, line in enumerate(file_content.rstrip().split('\n')):
        if re.match(r'^```.*', line):
            code_flag = 1 if code_flag == 0 else 0
        if not header_pattern.match(line):
            out += line + "\n"
            continue

        groups = header_pattern.findall(line)[0]
        front_space = groups[0]
        header = groups[1]
        title = groups[2]

        if code_flag:
            out += "{}{} {}\n".format(front_space, header, title)
        else:
            if len(front_space) >= 4:
                error("too much space(s) in front of header !",
                      infile=file_name, line_nb=idx)
            if len(front_space) > 0:
                error("space(s) in front of header !",
                      Warn=True, infile=file_name, line_nb=idx)
            out += "{} {}\n".format(header, title)
    return (out)

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


def insert_bootcamp_title(args):
    """
    Insert bootcamp title to the template file.

    Args:
        args (undefined):

    """
    idx = get_line_containing("tmp/template.latex", "bootcamp_title")
    insert_line("tmp/template.latex", idx,  args.bootcamp_title)


def insert_day_title(args):
    """
    Insert day title to the template file.

    Args:
        args (undefined):

    """
    idx = get_line_containing("tmp/template.latex", "day_number")
    insert_line("tmp/template.latex", idx, args.day_title.split(' - ')[0])
    idx = get_line_containing("tmp/template.latex", "day_title")
    insert_line("tmp/template.latex", idx, args.day_title.split(' - ')[1])

# CONVERT BLANK CODE BLOCKS TO TXT
#####################################


def change_empty_code_block_style(file_name: str, file_content: str):
    """
    Change the empty block format to txt.

    Args:
        file_name (str): file name
        file_content (str): file content

    """
    out = ""

    if len(file_content) == 0:
        error("empty file !", infile=file_name)

    code_flag = 0
    code_flag_line = 0
    code_pattern = re.compile(r'^```(.*)')
    for idx, line in enumerate(file_content.rstrip().split('\n')):
        if not code_pattern.match(line):
            out += line + "\n"
            continue

        language = code_pattern.findall(line)[0]

        if code_flag:
            out += "```\n"
            code_flag = 0
            continue

        if len(language) == 0:
            out += "```txt\n"
        else:
            if language.strip() not in ['console', 'bash', 'sh',
                                        'zsh', 'python', 'py', 'txt']:
                error("unsupported language ! (supported languages are: 'console', \
'bash', 'sh', 'zsh', 'python', 'py', 'txt')",
                      infile=file_name, line_nb=idx)

            if language.strip() in ['py', 'python']:
                out += "```{}\n".format(language)
            else:
                out += "```txt\n"
        code_flag = 1
        code_flag_line = idx
    if code_flag:
        error("could not find closing code snippet !",
              infile=file_name, line_nb=code_flag_line)

    return (out)

# FORMAT LIST
################


def change_list_format(file_name: str, file_content: str):
    """
    Change and check the list format.

    Args:
        file_name (str): file name
        file_content (str): file content

    """
    out = ""

    if len(file_content) == 0:
        error("empty file !", infile=file_name)

    code_flag = 0
    equation_flag = 0
    prev_list = 0
    list_factor = 4
    list_pattern = re.compile(r'([\s]*)- (.*)')
    for idx, line in enumerate(file_content.rstrip().split('\n')):
        if re.match(r'^```.*', line):
            code_flag = 1 if code_flag == 0 else 0

        if re.match(r'^[\$]{2}.*', line):
            equation_flag = 1 if equation_flag == 0 else 0

        if not list_pattern.match(line) or code_flag or equation_flag:
            out += line + "\n"
            prev_list = 0
            continue

        groups = list_pattern.findall(line)[0]
        front_space = groups[0]

        if len(front_space) % list_factor != 0:
            error("number of spaces in front of list is not a factor of {} !"
                  .format(list_factor), infile=file_name, line_nb=idx)

        if prev_list:
            out += "\n"

        out += line + "\n"
        prev_list = 1

    return (out)

# FORMAT EQUATIONS
##################


def change_equations_format(file_name: str, file_content: str):
    """
    Change and check the format of equations.

    Args:
        file_name (str): file name
        file_content (str): file content

    """
    out = ""

    if len(file_content) == 0:
        error("empty file !", infile=file_name)

    eq_flag = 0
    eq_flag_line = 0
    eq_pattern = re.compile(r'^[\$]{2}(.*)')
    for idx, line in enumerate(file_content.rstrip().split('\n')):
        line = line.replace('\\frac', '\\cfrac')
        if not eq_pattern.match(line):
            out += line + "\n"
            continue

        if eq_flag:
            out += "$$\n\\normalsize\n"
            eq_flag = 0
            continue
        out += "\\large\n$$\n"

        eq_flag = 1
        eq_flag_line = idx
    if eq_flag:
        error("could not find closing equation mark !",
              infile=file_name, line_nb=eq_flag_line)

    return (out)

# SET URL COLOR
##################


def set_url_color(file_name: str, file_content: str):
    """
    Add url parameters for pdf build.

    Args:
        file_name (str): file name
        file_content (str): file content

    """
    out = "---\ncolorlinks: true\nurlcolor: \"blue\"\n---\n\n"

    if len(file_content) == 0:
        error("empty file !", infile=file_name)
    for idx, line in enumerate(file_content.rstrip().split('\n')):
        out += line + "\n"
    return (out)

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
