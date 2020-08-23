import pytest
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,parentdir+"/pdf_builder/")

from pdf_builder import check_bootcamp_title,\
                        check_day_title,\
                        change_img_format,\
                        change_header_format,\
                        change_list_format,\
                        change_empty_code_block_style,\
                        change_equations_format


class Test_check_bootcamp_title:
    def test_none_title(self):
        try:
            res = check_bootcamp_title(None)
            assert res == True
        except Exception as e:
            assert str(e) == '[Error] :: invalid bootcamp title length ! (length must be between 3 and 20)'

    def test_empty_title(self):
        try:
            res = check_bootcamp_title('')
            assert res == True
        except Exception as e:
            assert str(e) == '[Error] :: invalid bootcamp title length ! (length must be between 3 and 20)'

    def test_short_title(self):
        try:
            res = check_bootcamp_title('ti')
            assert res == True
        except Exception as e:
            assert str(e) == '[Error] :: invalid bootcamp title length ! (length must be between 3 and 20)'

    def test_long_title(self):
        try:
            res = check_bootcamp_title('abcdefghijklmnopqrstuvwxyz')
            assert res == True
        except Exception as e:
            assert str(e) == '[Error] :: invalid bootcamp title length ! (length must be between 3 and 20)'
    
    def test_spec_char_title(self):
        try:
            res = check_bootcamp_title('res->/?fft')
            assert res == True
        except Exception as e:
            assert str(e) == '[Error] :: invalid bootcamp title chars ([A-Za-z ] allowed)'

    def test_title_ok_1(self):
        try:
            res = check_bootcamp_title('Python')
            assert res == True
        except Exception as e:
            assert str(e) == ''
    
    def test_title_ok_2(self):
        try:
            res = check_bootcamp_title('Machine Learning')
            assert res == True
        except Exception as e:
            assert str(e) == ''
    
    def test_title_ok_3(self):
        try:
            res = check_bootcamp_title('Data Engineering')
            assert res == True
        except Exception as e:
            assert str(e) == ''

class Test_check_day_title:
    def test_none_title(self):
        try:
            res = check_day_title(None)
            assert res == True
        except Exception as e:
            assert str(e) == '[Error] :: invalid day title length ! (length must be between 11 and 40)'

    def test_empty_title(self):
        try:
            res = check_day_title('')
            assert res == True
        except Exception as e:
            assert str(e) == '[Error] :: invalid day title length ! (length must be between 11 and 40)'

    def test_short_title(self):
        try:
            res = check_day_title('Day00 - Dd')
            assert res == True
        except Exception as e:
            assert str(e) == '[Error] :: invalid day title length ! (length must be between 11 and 40)'

    def test_long_title(self):
        try:
            res = check_day_title('Day00 - abcdefghijklmnopqrstuvwxyz0123456789')
            assert res == True
        except Exception as e:
            assert str(e) == '[Error] :: invalid day title length ! (length must be between 11 and 40)'
    
    def test_spec_char_title(self):
        try:
            res = check_day_title('Day00 - abcdefghijklmnopqrstuvwxyz?')
            assert res == True
        except Exception as e:
            assert str(e) == '[Error] :: invalid day title chars ([A-Za-z -] allowed)'
    
    def test_format_title(self):
        try:
            res = check_day_title('Day - abcdefghijklmnopqrstuvwxyz?')
            assert res == True
        except Exception as e:
            assert str(e) == '[Error] :: invalid day title ! (it must be formatted as follows \"DayXX - ...\")'

    def test_title_ok_1(self):
        try:
            res = check_day_title('Day00 - PostgreSQL')
            assert res == True
        except Exception as e:
            assert str(e) == ''
    
    def test_title_ok_2(self):
        try:
            res = check_day_title('Day01 - Elasticsearch Logstash Kibana')
            assert res == True
        except Exception as e:
            assert str(e) == ''

class Test_change_img_format:
    def test_empty_file(self):
        try:
            res = change_img_format("toto.md", "")
            assert res == ""
        except Exception as e:
            assert str(e) == '[Error] toto.md :: empty file !'

    def test_empty_image_title(self):
        try:
            res = change_img_format("toto.md", "![](path)")
            assert res == "\n![path](tmp/assets/path)\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_empty_image_path(self):
        try:
            res = change_img_format("toto.md", "![title]()")
            assert res == ""
        except Exception as e:
            assert str(e) == '[Error] toto.md:1 :: empty image path !'
    
    def test_empty_image_style(self):
        try:
            res = change_img_format("toto.md", r"![title](path)\{\}")
            assert res == "\n![title](tmp/assets/path)\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_image_md_style_ko(self):
        try:
            res = change_img_format("toto.md", "![title](path){width=450x}")
            assert res == ""
        except Exception as e:
            assert str(e) == "[Error] toto.md:1 :: wrong image style format ! (example: '{width=250px}')"

    def test_image_md_ok(self):
        try:
            res = change_img_format("toto.md", "![title](path){width=450px}\n")
            assert res == "\n![title](tmp/assets/path){width=450px}\n"
        except Exception as e:
            assert str(e) == ""

    def test_empty_html_image_title(self):
        try:
            res = change_img_format("toto.md", "<img src='src/toto.png' />\n")
            assert res == "\n![toto](tmp/assets/toto.png)\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_empty_html_image_title2(self):
        try:
            res = change_img_format("toto.md", """<img src="src/toto.png" />\n""")
            assert res == "\n![toto](tmp/assets/toto.png)\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_empty_html_image_path(self):
        try:
            res = change_img_format("toto.md", "<img src='' />\n")
            assert res == ""
        except Exception as e:
            assert str(e) == '[Error] toto.md:1 :: empty image path !'
    
    def test_empty_html_image_space_front(self):
        try:
            res = change_img_format("toto.md", " <img src='src/toto.png' />\n")
            assert res == "\n![toto](tmp/assets/toto.png)\n"
        except Exception as e:
            assert str(e) == '[Error] toto.md:1 :: empty image path !'
    
    def test_empty_image_space_front(self):
        try:
            res = change_img_format("toto.md", " ![toto](src/toto.png){width=450px}\n")
            assert res == "\n![toto](tmp/assets/toto.png){width=450px}\n"
        except Exception as e:
            assert str(e) == '[Error] toto.md:1 :: empty image path !'
    
    def test_no_images_multi_lines(self):
        try:
            res = change_img_format("toto.md", """\n\n1\n\n2\n\n""")
            assert res == "\n\n1\n\n2\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_images_multi_lines(self):
        try:
            res = change_img_format("toto.md", """1\n\n![toto](src/toto.png){width=450px}\n\n2\n""")
            assert res == "1\n\n\n![toto](tmp/assets/toto.png){width=450px}\n\n2\n"
        except Exception as e:
            assert str(e) == '[Error] toto.md:1 :: empty image path !'

class Test_change_header_format:
    def test_empty_file(self):
        try:
            res = change_header_format("toto.md", "")
            assert res == ""
        except Exception as e:
            assert str(e) == '[Error] toto.md :: empty file !'
    
    def test_header_1(self):
        try:
            res = change_header_format("toto.md", "# header\n")
            assert res == "# header\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_header_4(self):
        try:
            res = change_header_format("toto.md", "#### header\n")
            assert res == "#### header\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_header_5(self):
        try:
            res = change_header_format("toto.md", "##### header\n")
            assert res == "##### header\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_header_4_space_front(_self):
        try:
            res = change_header_format("toto.md", "    ####  header\n")
            assert res == "#### header\n"
        except Exception as e:
            assert str(e) == '[Error] toto.md:1 :: too much space(s) in front of header !'
    
    def test_header_5_space_front(self):
        try:
            res = change_header_format("toto.md", "     ##### header\n")
            assert res == "     ##### header\n"
        except Exception as e:
            assert str(e) == '[Error] toto.md:1 :: too much space(s) in front of header !'
    
    def test_header_4_space_back(_self):
        try:
            res = change_header_format("toto.md", "####    header\n")
            assert res == "#### header\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_comment_in_block(self):
        try:
            res = change_header_format("toto.md", "\n\n```\n    ## hello\n```\nheader\n")
            assert res == "\n\n```\n    ## hello\n```\nheader\n"
        except Exception as e:
            assert str(e) == ''

class Test_change_list_format:
    def test_empty_file(self):
        try:
            res = change_list_format("toto.md", "")
            assert res == ""
        except Exception as e:
            assert str(e) == '[Error] toto.md :: empty file !'
    
    def test_list_1(self):
        try:
            res = change_list_format("toto.md", "l1\n- ttt\nl3\n")
            assert res == "l1\n\n- ttt\nl3\n"
        except Exception as e:
            assert str(e) == ''

    def test_list_2(self):
        try:
            res = change_list_format("toto.md", "l1\n- ttt\n- aaa\nl3\n")
            assert res == "l1\n\n- ttt\n\n- aaa\nl3\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_list_2_bis(self):
        try:
            res = change_list_format("toto.md", "l1\n- ttt\n\n- aaa\nl3\n")
            assert res == "l1\n\n- ttt\n\n- aaa\nl3\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_list_2_dots(self):
        try:
            res = change_list_format("toto.md", "l1:\n* ttt\n\n* aaa\nl3\n")
            assert res == "l1:\n\n* ttt\n\n* aaa\nl3\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_list_inner_1(self):
        try:
            res = change_list_format("toto.md", "l1\n- ttt\n\n- aaa\n    - bbb\n- ccc\nl3\n")
            assert res == "l1\n\n- ttt\n\n- aaa\n\n    - bbb\n\n- ccc\nl3\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_list_inner_1_wrong_factor(self):
        try:
            res = change_list_format("toto.md", "l1\n- ttt\n\n- aaa\n   - bbb\n- ccc\nl3\n")
            assert res == ""
        except Exception as e:
            assert str(e) == '[Error] toto.md:5 :: number of spaces in front of list is not a factor of 4 !'
    
    def test_list_inner_2(self):
        try:
            res = change_list_format("toto.md", "l1\n- ttt\n\n- aaa\n    - bbb\n        - ddd\n    - eee\n- ccc\nl3\n")
            assert res == "l1\n\n- ttt\n\n- aaa\n\n    - bbb\n\n        - ddd\n\n    - eee\n\n- ccc\nl3\n"
        except Exception as e:
            assert str(e) == ''
        
    def test_list_inner_2_wrong_factor(self):
        try:
            res = change_list_format("toto.md", "l1\n- ttt\n\n- aaa\n    - bbb\n         - ddd\n    - eee\n- ccc\nl3\n")
            assert res == ""
        except Exception as e:
            assert str(e) == '[Error] toto.md:6 :: number of spaces in front of list is not a factor of 4 !'
    
    def test_list_stars(self):
        try:
            res = change_list_format("toto.md", "`cookbook` will store 3 recipes:\n* sandwich\n* cake\n* salad\n")
            assert res == "`cookbook` will store 3 recipes:\n\n* sandwich\n\n* cake\n\n* salad\n"
        except Exception as e:
            assert str(e) == ''

    def test_list_in_code(self):
        try:
            res = change_list_format("toto.md", "l1\n```\n- ttt\n  - aaa\n```\nl3\n")
            assert res == "l1\n```\n- ttt\n  - aaa\n```\nl3\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_list_in_equation(self):
        try:
            res = change_list_format("toto.md", "l1\n$$\n- ttt\n  - aaa\n$$\nl3\n")
            assert res == "l1\n$$\n- ttt\n  - aaa\n$$\nl3\n"
        except Exception as e:
            assert str(e) == ''
    
class Test_change_empty_block_style:
    def test_empty_file(self):
        try:
            res = change_empty_code_block_style("toto.md", "")
            assert res == ""
        except Exception as e:
            assert str(e) == '[Error] toto.md :: empty file !'
    
    def test_python_block(self):
        try:
            res = change_empty_code_block_style("toto.md", "dd\n```python\ndd\n```\ndd\n")
            assert res == "dd\n```python\ndd\n```\ndd\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_bash_block(self):
        try:
            res = change_empty_code_block_style("toto.md", "dd\n```bash\ndd\n```\ndd\n")
            assert res == "dd\n```txt\ndd\n```\ndd\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_sh_block(self):
        try:
            res = change_empty_code_block_style("toto.md", "dd\n```sh\ndd\n```\ndd\n")
            assert res == "dd\n```txt\ndd\n```\ndd\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_console_block(self):
        try:
            res = change_empty_code_block_style("toto.md", "dd\n```console\ndd\n```\ndd\n")
            assert res == "dd\n```txt\ndd\n```\ndd\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_empty_block(self):
        try:
            res = change_empty_code_block_style("toto.md", "dd\n```\ndd\n```\ndd\n")
            assert res == "dd\n```txt\ndd\n```\ndd\n"
        except Exception as e:
            assert str(e) == ''

    def test_wrong_block_number(self):
        try:
            res = change_empty_code_block_style("toto.md", "dd\n```\ndd\n```\ndd\n```\ndd\n")
            assert res == ""
        except Exception as e:
            assert str(e) == '[Error] toto.md:6 :: could not find closing code snippet !'
    
    def test_multiple_code_blocks(self):
        try:
            res = change_empty_code_block_style("toto.md", "dd\n```\ndd\n```\ndd\n```python\ndd\n```\ndd\n```\ndd\n```\ndd\n")
            assert res == "dd\n```txt\ndd\n```\ndd\n```python\ndd\n```\ndd\n```txt\ndd\n```\ndd\n"
        except Exception as e:
            assert str(e) == '[Error] toto.md :: empty file !'

class Test_format_equations:
    def test_empty_file(self):
        try:
            res = change_equations_format("toto.md", "")
            assert res == ""
        except Exception as e:
            assert str(e) == '[Error] toto.md :: empty file !'
    
    def test_frac_replace(self):
        try:
            res = change_equations_format("toto.md", "dd\n$$\n\\frac{1/0}\n$$\ndd\n")
            assert res == "dd\n\\large\n$$\n\\cfrac{1/0}\n$$\n\\normalsize\ndd\n"
        except Exception as e:
            assert str(e) == ''
    
    def test_wrong_number_eq_mark(self):
        try:
            res = change_equations_format("toto.md", "dd\n$$\n\\frac{1/0}\n$$\ndd\n$$\ndd\n")
            assert res == ""
        except Exception as e:
            assert str(e) == '[Error] toto.md:6 :: could not find closing equation mark !'
