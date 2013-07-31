#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* Date: 29.07.13
* Time: 18:56
* Original filename: 
"""

from __future__ import absolute_import, print_function
import optdict

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='OptDict',
      version=optdict.__version__,
      author=optdict.__author__,
      author_email='me@mosquito.su',
      license="MIT",
      summary="OptDict module",
      description="OptDict - Option parser from dictionary, with configure from file and validation.",
      platform="all",
      home_page="http://github.com/mosquito/optdict",
      packages=[
          'optdict',
      ],
)