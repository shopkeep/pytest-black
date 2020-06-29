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
    python_requires=">=2.7",
    install_requires=[
        "pytest>=3.5.0",
        # Minimum requirement on black 19.3b0 or later is not declared here as
        # workaround for https://github.com/pypa/pipenv/issues/3928
        'black; python_version >= "3.6"',
        "toml",
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["black = pytest_black"]},
)
