#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* Created by PyCharm.
* Date: 30.07.13
* Time: 14:27
* Original filename: 
"""

__author__ = 'mosquito'

from optdict import Parser, validators

options_dict = {
    # Params section "main"
    "main": {
        "listen": {
            # Command line keys (require)
            "keys": ["-l", "--listen"],

            # Validator call for value (optional)
            "validator": validators.Valid(lambda addr: ".".join([str(j) for j in [int(i) for i in addr.split(".")] if j >=0 and j<256]) == addr),

            # Help text (optional)
            "help": "Listen address",

            # Default value (optional default None)
            "default": "127.0.0.1",

            # Action (optional)
            # support all OptParse options
            # * store_true - stores true (default False)
            # * store_false - stores false (default True)
            # * store_const - stores constans
            # * count - stores the number of repetitions of the key (if only key is single symbol)
            "action": "store_const"
        }
    },
    # Another section
    "debug": {
        "debug": {
            "keys": ['-d'],
            "action": "count",
            "default": 0,
            "type": "int",
            "help": "Debuging output"
        }
    },
    # Meta section
    "__meta__": {
        # Help messages for sections
        "sections_help": {
            "debug": "Debugging options",
            "main": "Main options"
        },
        "sections_text": {
            "main": "This section contains main options for test this..."
        }
    }
}

if __name__ == "__main__":
    options, args = Parser(options_dict).parse_args()