
import re
import os
import sys
import inspect
from utils import sub_run


currentdir = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe()))
)
sys.path.insert(0, currentdir+"/pdf_builder")


OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def clone_branch(repo, branch):
    sub_run("git clone -b {} https://github.com/42-AI/{}.git"
            .format(branch, repo))


def main():
    repos = {
        "bootcamp_python": "master",
        "bootcamp_machine-learning": "master",
        "bootcamp_data-engineering": "master"
    }
    for _dir, _branch in repos.items():
        clone_branch(_dir, _branch)
    for _dir in repos:
        days = {}
        res = sub_run("ls -d {}/day*/".format(_dir)).stdout.decode().strip()
        for d in res.split('\n'):
            days[d.split('/')[1]] = d
        for k, v in days.items():
            dd = "{}.{}.pdf".format(_dir, k)
            res = sub_run("python3 pdf_builder -b \"{}\" -d {} -t \
                        \"Day00 - ddd\" -o {}".format(_dir.replace('_', ' ')
                                                      .replace('-', ' '),
                                                      v, dd))

            pattern = re.compile(r'(Successfully.*?!)')
            if pattern.findall(res.stderr.decode().strip()):
                print("{}SUCCESS{}!".format(OKGREEN, ENDC))
            else:
                print("{}ERROR{}!".format(FAIL, ENDC))
                print(res.stdout.decode().strip())
    res = sub_run("python3 pdf_builder -b \"Data Engineering\" \
                   -f bootcamp_data-engineering/day00/ex03/psycopg2_basics.md \
                   -t \"Day00 - ddd\" -o \
                       bootcamp_data-engineering.psycopg2_doc.pdf")
    pattern = re.compile(r'(Successfully.*?!)')
    if pattern.findall(res.stderr.decode().strip()):
        print("{}SUCCESS{}!".format(OKGREEN, ENDC))
    else:
        print("{}ERROR{}!".format(FAIL, ENDC))
        print(res.stderr.decode())
        pattern = re.compile(r'Detected!.*?$', re.DOTALL)
        print("\n".join(pattern.findall(res.stderr.decode()
                                        .strip())[0].split('\n')[1:]))


if __name__ == "__main__":
    main()
