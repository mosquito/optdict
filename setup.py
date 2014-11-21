#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
import optdict

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = """
OptDict
=======

Python module for easy to use command line options. With validation options
values and configuration from JSON file.

Validations
-----------

The module provides this validators:

* RequireAll(func1[, func2, ... funcN]) {synonym: Require}
* RequireOnce(func1[, func2, ... funcN])
* ValidAll(name1[, name2 ... nameN]) {synonym: Valid}
* ValidOnce(name1[, name2 ... nameN])
* Conflict(name1[, name2 ... nameN])
* ValidationQueue(Validator0[, Validator1])
"""

setup(
    name='OptDict',
    version=optdict.__version__,
    author=optdict.__author__,
    author_email='me@mosquito.su',
    license="MIT",
    description="OptDict - Option parser from dictionary, with configure from file and validation.",
    platforms="all",
    url="http://github.com/mosquito/optdict",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        "Programming Language :: Python",
    ],
    long_description=long_description,
    packages=[
        'optdict',
    ],
)
