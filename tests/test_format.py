import pytest

from pdf_builder.params_check import \
    check_bootcamp_title,\
    check_day_title

from pdf_builder.files_formatting import \
    change_img_format,\
    change_header_format,\
    change_list_format,\
    change_equations_format,\
    change_empty_code_block_style

class Test_check_bootcamp_title:

    @pytest.mark.parametrize("bootcamp_title", [
        None,
        "",
        "ti",
        "abcdefghijklmnopqrstuvwxyz"
    ])
    def test_bootcamp_title_error_length(self, bootcamp_title):
        with pytest.raises(Exception, match=r".* invalid bootcamp title length .*"):
            check_bootcamp_title(bootcamp_title)

    def test_bootcamp_title_error_char(self):
        with pytest.raises(Exception, match=r".* invalid bootcamp title chars .*"):
            check_bootcamp_title("res->/?fft")

    @pytest.mark.parametrize("bootcamp_title", [
        "Python",
        "Machine Learning",
        "Data Engineering"
    ])
    def test_bootcamp_title_ok(self, bootcamp_title):
        assert check_bootcamp_title(bootcamp_title) == True


class Test_check_day_title:

    @pytest.mark.parametrize("day_title", [
        None,
        "",
        "Day00 - Dd",
        "Day00 - abcdefghijklmnopqrstuvwxyz0123456789"
    ])
    def test_day_title_error_length(self, day_title):
        with pytest.raises(Exception, match=r".* invalid day title length .*"):
            check_day_title(day_title)

    def test_day_title_error_char(self):
        with pytest.raises(Exception, match=r".* invalid day title chars .*"):
            check_day_title('Day00 - abcdefghijklmnopqrstuvwxyz?')
    
    def test_day_title_error(self):
        with pytest.raises(Exception, match=r".* invalid day title format .*"):
            check_day_title('Day - abcdefghijklmnopqrstuvwxyz')
    
    @pytest.mark.parametrize("day_title", [
        "Day00 - PostgreSQL",
        "Day01 - Elasticsearch Logstash Kibana"
    ])
    def test_day_title_error_length(self, day_title):
        assert check_day_title(day_title) == True


class Test_change_img_format:
    @pytest.mark.parametrize("line", [
        "![title]()",
        "<img src='' />\n"
    ])
    def test_empty_image_path(self, line):
        with pytest.raises(Exception, match=r".* toto.md.*? :: empty image path .*"):
            change_img_format("toto.md", line)

    @pytest.mark.parametrize("line,expected", [
        ("![](path)",                                       "\n![path](tmp/assets/path)\n"),
        ("![title](path){}".format(""),                              "\n![title](tmp/assets/path)\n"),
        ("![title](path){width=450px}\n",                   "\n![title](tmp/assets/path){width=450px}\n"),
        ("<img src='src/toto.png' />\n",                    "\n![toto](tmp/assets/toto.png)\n"),
        (" <img src='src/toto.png' />\n",                   "\n![toto](tmp/assets/toto.png)\n"),
        (" ![toto](src/toto.png){width=450px}\n",           "\n![toto](tmp/assets/toto.png){width=450px}\n"),
        ("\n\n1\n\n2\n\n",                                  "\n\n1\n\n2\n"),
        ("1\n\n![toto](src/toto.png){width=450px}\n\n2\n", "1\n\n\n![toto](tmp/assets/toto.png){width=450px}\n\n2\n")
    ])
    def test_image_path_ok(self, line, expected):
        assert change_img_format("toto.md", line) == expected

    def test_image_format_error(self):
        with pytest.raises(Exception, match=r".* toto.md.*? :: wrong image style format .*"):
            change_img_format("toto.md", "![title](path){width=450x}")

class Test_change_header_format:
    def test_change_header_empty_file(self):
        with pytest.raises(Exception, match=r".* toto.md.*? :: empty file .*"):
            change_header_format("toto.md", "")

    @pytest.mark.parametrize("line,expected", [
        ("# header\n",                           "# header\n"),
        ("#### header\n",                        "#### header\n"),
        ("##### header\n",                       "##### header\n"),
        ("     ##### header\n",                  "     ##### header\n"),
        ("####    header\n",                     "#### header\n"),
        ("\n\n```\n    ## hello\n```\nheader\n", "\n\n```\n    ## hello\n```\nheader\n")
    ])
    def test_change_header_ok(self, line, expected):
        assert change_header_format("toto.md", line) == expected

    def test_change_header_space_error(self):
        with pytest.raises(Exception, match=r".* toto.md.*? :: too much space\(s\) in front of header .*"):
            change_header_format("toto.md", "    ####  header\n")

class Test_change_list_format:
    def test_empty_file(self):
        with pytest.raises(Exception, match=r".* toto.md.*? :: empty file .*"):
            change_list_format("toto.md", "")

    @pytest.mark.parametrize("lines,expected", [
        ("l1\n- ttt\nl3\n",        "l1\n\n- ttt\nl3\n"),
        ("l1\n- ttt\n- aaa\nl3\n", "l1\n\n- ttt\n\n- aaa\nl3\n"),
        ("l1\n- ttt\n\n- aaa\nl3\n", "l1\n\n- ttt\n\n- aaa\nl3\n"),
        ("l1:\n* ttt\n\n* aaa\nl3\n", "l1:\n\n* ttt\n\n* aaa\nl3\n"),
        ("l1\n- ttt\n\n- aaa\n    - bbb\n- ccc\nl3\n", "l1\n\n- ttt\n\n- aaa\n\n    - bbb\n\n- ccc\nl3\n"),
        ("l1\n- ttt\n\n- aaa\n    - bbb\n        - ddd\n    - eee\n- ccc\nl3\n", "l1\n\n- ttt\n\n- aaa\n\n    - bbb\n\n        - ddd\n\n    - eee\n\n- ccc\nl3\n"),
        ("`cookbook` will store 3 recipes:\n* sandwich\n* cake\n* salad\n", "`cookbook` will store 3 recipes:\n\n* sandwich\n\n* cake\n\n* salad\n"),
        ("l1\n```\n- ttt\n  - aaa\n```\nl3\n", "l1\n```\n- ttt\n  - aaa\n```\nl3\n"),
        ("l1\n$$\n- ttt\n  - aaa\n$$\nl3\n", "l1\n$$\n- ttt\n  - aaa\n$$\nl3\n")
    ])
    def test_list_ok(self, lines, expected):
        assert change_list_format("toto.md", lines) == expected
    
    @pytest.mark.parametrize("lines", [
        "l1\n- ttt\n\n- aaa\n   - bbb\n- ccc\nl3\n",
        "l1\n- ttt\n\n- aaa\n    - bbb\n         - ddd\n    - eee\n- ccc\nl3\n"
    ])
    def test_empty_file(self, lines):
        with pytest.raises(Exception, match=r".* toto.md.*? :: number of spaces in front of list is not a factor of 4 .*"):
            change_list_format("toto.md", lines)
    
class Test_change_empty_block_style:

    def test_empty_file(self):
        with pytest.raises(Exception, match=r".* toto.md.*? :: empty file.*"):
            change_empty_code_block_style("toto.md", "")
    
    @pytest.mark.parametrize("lines,expected", [
        ("dd\n```python\ndd\n```\ndd\n", "dd\n```python\ndd\n```\ndd\n"),
        ("dd\n```sh\ndd\n```\ndd\n", "dd\n```txt\ndd\n```\ndd\n"),
        ("dd\n```console\ndd\n```\ndd\n", "dd\n```txt\ndd\n```\ndd\n"),
        ("dd\n```\ndd\n```\ndd\n```python\ndd\n```\ndd\n```\ndd\n```\ndd\n", "dd\n```txt\ndd\n```\ndd\n```python\ndd\n```\ndd\n```txt\ndd\n```\ndd\n")
    ])
    def test_python_block_ok(self, lines, expected):
        assert change_empty_code_block_style("toto.md", lines) == expected

    def test_wrong_block_number(self):
        with pytest.raises(Exception, match=r".* toto.md.*? :: could not find closing code snippet .*"):
            change_empty_code_block_style("toto.md", "dd\n```\ndd\n```\ndd\n```\ndd\n")

class Test_format_equations:
    def test_empty_file(self):
        with pytest.raises(Exception, match=r".* toto.md.*? :: empty file .*"):
            change_equations_format("toto.md", "")
    
    def test_frac_replace(self):
        res = change_equations_format("toto.md", "dd\n$$\n\\frac{1/0}\n$$\ndd\n")
        assert res == "dd\n\\large\n$$\n\\cfrac{1/0}\n$$\n\\normalsize\ndd\n"
    
    def test_wrong_number_eq_mark(self):
        with pytest.raises(Exception, match=r".* toto.md.*? :: could not find closing equation mark .*"):
            change_equations_format("toto.md", "dd\n$$\n\\frac{1/0}\n$$\ndd\n$$\ndd\n")
