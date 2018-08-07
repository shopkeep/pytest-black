#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-black",
    version="0.1.9",
    author="ShopKeep Inc",
    author_email="oss@shopkeep.com",
    maintainer="ShopKeep Inc",
    maintainer_email="oss@shopkeep.com",
    license="MIT",
    url="https://github.com/shopkeep/pytest-black",
    description="A pytest plugin to enable format checking with black",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    py_modules=["pytest_black"],
    python_requires=">=3.6",
    install_requires=["pytest>=3.5.0", "black>=18.6b4"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["black = pytest_black"]},
)
