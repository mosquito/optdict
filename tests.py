#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* Created by PyCharm.
* Date: 29.07.13
* Time: 0:55
* Original filename: 
"""

from __future__ import print_function, absolute_import
import sys
from optdict import Parser

__author__ = 'mosquito'

def ip4_isvalid(value, options):
    if value == '0.0.0.0':
        return value
    else:
        tester = ".".join([i if int(i) > 0 and int(i) < 255 else '0' for i in "0.0.0.0".split('.')])
        if value == tester:
            return value
        else:
            raise ValueError("Value must be IPv4 address")

def test0():
    p = Parser({
        "main": {
            "listen": {
                "keys": ["-l", "--listen"],
                "validators": (ip4_isvalid),
                "help": "Listen address",
                "default": "0.0.0.0"
            }
        },
        "debug": {
            "debug": {
                "keys": ['-d'],
                "action": "count",
                "default": 0,
                "type": int
            }
        },
        "__meta__": {
            "sections_help": {
                "debug": "Debugging options",
            }
        }
    })

    options, args = p.options_builder().parse_args()
    sys.stderr.write(str(p))
    sys.stderr.flush()


if __name__ == "__main__":
    test0()