#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* Date: 29.07.13
* Time: 0:55
* Original filename: 
"""

from __future__ import print_function, absolute_import
import sys
from optdict import Parser, validators

__author__ = 'mosquito'

def log(*args):
    for i in args:
        sys.stderr.write("{0}\n".format(str(i)))
    sys.stderr.flush()

options, args = (None, None)

def test_000_optons():
    global options, args

    p = Parser({
        "main": {
            "listen": {
                "keys": ["-l", "--listen"],
                "validator": validators.ValidAll(lambda addr: ".".join([str(j) for j in [int(i) for i in addr.split(".")] if j >=0 and j<256]) == addr),
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

    options, args = p.parse_args()
    log(p)

def validator_run(func, key="debug", value=None):
    global options, args
    func(arg=value, options=options, parser=None, dest=key)
    return True

def test_001_valid_once():
    assert validator_run(validators.ValidOnce(lambda x: x > 0, lambda x: x < 256), "debug", 1024)
    try:
        validator_run(validators.ValidOnce(lambda x: x > 0, lambda x: x < 256), "debug", -10)
    except validators.ValidationError:
        return

def test_002_valid_all():
    assert validator_run(validators.ValidAll(lambda x: x > 0, lambda x: x < 256), "debug", 128)
    try:
        validator_run(validators.ValidAll(lambda x: x > 0, lambda x: x < 256), "debug", 1024)
    except validators.ValidationError:
        return

def test_003_require_once():
    assert validator_run(validators.RequireOnce("main_listen"), value=1)
    try:
        validator_run(validators.RequireOnce("listen"), value=1)
    except validators.ValidationError:
        return

def test_004_conflict_param():
    assert validator_run(validators.Conflict("listen"))
    try:
        validator_run(validators.Conflict("main_listen", critical=True))
    except validators.ValidationError:
        return

if __name__ == "__main__":
    for func in dir():
        if func.startswith("test_"):
            log("Run test: {0}".format(func))
            getattr(sys.modules[__name__], func)()