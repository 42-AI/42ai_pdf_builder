
#import importlib
#importlib.reload(..pdf_builder)
#from pdf_builder.params_check import *

#print(sys.path)
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,parentdir+"/pdf_builder")

#print(sys.path)
# import sys
# sys.path.insert(0,'..')
import pdf_builder.params_check as params_check
import pdf_builder.utils

def test_title_empty():
	bootcamp_title = ""
	try:
		res = params_check.check_bootcamp_title(bootcamp_title)
	except Exception as e:
		res = str(e)
	assert res == "Error :: title too short (< 3 chars)"

def test_title_too_short():
	bootcamp_title = "dd"
	try:
		res = params_check.check_bootcamp_title(bootcamp_title)
	except Exception as e:
		res = str(e)
	assert res == "Error :: title too short (< 3 chars)"

def test_title_too_long():
	bootcamp_title = "dddddddddrfsfsfefsfeukfhuhfeuskhfeukhfsuk"
	try:
		res = params_check.check_bootcamp_title(bootcamp_title)
	except Exception as e:
		res = str(e)
	assert res == "Error :: invalid title len (> 30 chars)"

def test_title_spec_chars():
	bootcamp_title = "dddd_ssds"
	try:
		res = params_check.check_bootcamp_title(bootcamp_title)
	except Exception as e:
		res = str(e)
	assert res == "Error :: invalid title chars ([A-Za-z ] allowed)"

def test_title_ok():
	bootcamp_title = "Data Engineering"
	try:
		res = params_check.check_bootcamp_title(bootcamp_title)
	except Exception as e:
		res = str(e)
	assert res is None

def test_dir_ok():
	input_dir = "tests/test_dirs/day00"
	try:
		res = params_check.check_input_dir(input_dir)
	except Exception as e:
		res = str(e)
	assert res == None

def test_dir_ok_2():
	input_dir = "tests/test_dirs/day00/"
	try:
		res = params_check.check_input_dir(input_dir)
	except Exception as e:
		res = str(e)
	assert res == None

def test_dir_day_missing():
	input_dir = "tests/test_dirs/day01"
	try:
		res = params_check.check_input_dir(input_dir)
	except Exception as e:
		res = str(e)
	assert res == "Error :: markdown for day missing"

def test_dir_ex_missing():
	input_dir = "tests/test_dirs/day02"
	try:
		res = params_check.check_input_dir(input_dir)
	except Exception as e:
		res = str(e)
	assert res == "Error :: markdown for exercices missing"

def test_dir_not_dir():
	input_dir = "./day03"
	try:
		res = params_check.check_input_dir(input_dir)
	except Exception as e:
		res = str(e)
	assert res == "Error :: './day03' is not a directory !"

def test_file_ok():
	input_file = "tests/test_dirs/day00/day00.md"
	try:
		res = params_check.check_input_file(input_file)
	except Exception as e:
		res = str(e)
	assert res == None

def test_file_markdown():
	input_file = "./day02/day01.md"
	try:
		res = params_check.check_input_file(input_file)
	except Exception as e:
		res = str(e)
	assert res == "Error :: './day02/day01.md' is not a file !"

def test_day_title_ok():
	day_title = "Day00 - xsxss"
	try:
		res = params_check.check_day_title(day_title)
	except Exception as e:
		res = str(e)
	assert res == None

def test_day_title_ko():
	day_title = "day00 - xsxss"
	try:
		res = params_check.check_day_title(day_title)
	except Exception as e:
		res = str(e)
	assert res == """Error :: \'day00 - xsxss\' invalid Day title (must be formatted as follows "DayXX - ...")"""
