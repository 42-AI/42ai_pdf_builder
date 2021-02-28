# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup, find_packages


setup (
    name = "pdf-builder",
    packages = find_packages(),
    entry_points = {
        "console_scripts": ['pdf-builder = pdf_builder.cli:cli']
        },
    version = '0.1.0',
    description = "Pdf-builder tool for the 42-AI projects",
    author = "Francois-Xavier Babin",
    author_email = "fbabin@student.42.fr",
    include_package_data=True,
    package_data={'': ['templates/*']},
    install_requires = ['click']
)