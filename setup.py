# !/usr/bin/env python
import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pdf_builder",
    version="1.0",
    author="Francois-Xavier Babin & Mathilde Boivin",
    description=("A pdf builder for 42-AI subjects"),
    license="MIT",
    packages=find_packages(),
    long_description=read('README.md'),
)
