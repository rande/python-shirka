#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name="ioc",
    version="0.0.1",
    description="A small bot based on twisted",
    author="Thomas Rabaix",
    author_email="thomas.rabaix@gmail.com",
    url="https://github.com/rande/python-shirka",
    py_modules=["shirka"],
    packages = ['shirka'],
    install_requires=["ioc", "twisted", "twistedhttpstream"],
)