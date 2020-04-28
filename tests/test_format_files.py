import re
import os,sys,inspect
import subprocess
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)


def sub_run(command):
	out = subprocess.run(command,
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE)
	return (out)


def test_code_block_ok():
	bootcamp_title = "Data Engineering"
	input_file = "tests/test_dirs/day00/code_block_ok.md"
	pdf_title = "Day00 - xxx"
	output_file = "day00.pdf"
	res = sub_run("""python pdf_builder -b "{}" -f {} -t "{}" -o {}
    """.format(bootcamp_title, input_file, pdf_title, output_file))
	pattern = re.compile(r'(Successfully created).*$')
	out = pattern.findall(res.stderr.decode().strip())
	assert "Successfully created" == out[0]

def test_code_block_ko():
	bootcamp_title = "Data Engineering"
	input_file = "tests/test_dirs/day00/code_block_ko.md"
	pdf_title = "Day00 - xxx"
	output_file = "day00.pdf"
	res = sub_run("""python pdf_builder -b "{}" -f {} -t "{}" -o {}
    """.format(bootcamp_title, input_file, pdf_title, output_file))
	pattern = re.compile(r'(TeX capacity exceeded)')
	out = pattern.findall(res.stdout.decode().strip())
	assert "TeX capacity exceeded" == out[0]

def test_img():
	bootcamp_title = "Data Engineering"
	input_file = "tests/test_dirs/day00/imgs.md"
	pdf_title = "Day00 - xxx"
	output_file = "day00.pdf"
	res = sub_run("""python pdf_builder -b "{}" -f {} -t "{}" -o {}
    """.format(bootcamp_title, input_file, pdf_title, output_file))
	pattern = re.compile(r'(Successfully created).*$')
	out = pattern.findall(res.stderr.decode().strip())
	assert "Successfully created" == out[0]

def test_links():
	bootcamp_title = "Data Engineering"
	input_file = "tests/test_dirs/day00/links.md"
	pdf_title = "Day00 - xxx"
	output_file = "day00.pdf"
	res = sub_run("""python pdf_builder -b "{}" -f {} -t "{}" -o {}
    """.format(bootcamp_title, input_file, pdf_title, output_file))
	pattern = re.compile(r'(Successfully created).*$')
	out = pattern.findall(res.stderr.decode().strip())
	assert "Successfully created" == out[0]

def test_lists():
	bootcamp_title = "Data Engineering"
	input_file = "tests/test_dirs/day00/lists.md"
	pdf_title = "Day00 - xxx"
	output_file = "day00.pdf"
	res = sub_run("""python pdf_builder -b "{}" -f {} -t "{}" -o {}
    """.format(bootcamp_title, input_file, pdf_title, output_file))
	pattern = re.compile(r'(Successfully created).*$')
	out = pattern.findall(res.stderr.decode().strip())
	assert "Successfully created" == out[0]
