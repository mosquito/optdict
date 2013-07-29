#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* Created by PyCharm.
* Date: 29.07.13
* Time: 0:12
* Original filename: 
"""

from __future__ import print_function, absolute_import
from inspect import isfunction
from optparse import OptionParser, OptionGroup, OptionValueError, OptionConflictError
import codecs
import json
import os

__author__ = 'mosquito'

class Parser(object):
    def __init__(self, dictionary):
        """
            def ip4_isvalid(value, options):
                if value == '0.0.0.0':
                    return value
                else:
                    tester = ".".join([i if int(i) > 0 and int(i) < 255 else '0' for i in "0.0.0.0".split('.')])
                    if value == tester:
                        return value
                    else:
                        raise ValueError("Value must be IPv4 address")

            dictionary = {
                "main": {
                    "listen_address": {
                        "keys": ["-l", "--listen"],
                        "validators": (ip4_isvalid),
                        "help": "Listen address",
                        "default": "0.0.0.0",
                        "action": "store_const"
                    }
                },
                "debug": {
                    "debug": {
                        "keys": ['-d'],
                        "action": "count",
                        "default": 0,
                        "type": "int",
                        "help": "Debuging output"
                    }
                },
                "__meta__": {
                    "sections_help": {
                        "debug": "Debugging options",
                        "main": "Main options"
                    }
                }
            }
        """

        assert isinstance(dictionary, dict)
        self.data = dictionary
        self.validate_dict()

    def __str__(self):
        return json.dumps((self._data_dict, self._sections_help), indent=1, default=lambda n: str(n))

    def validate_dict(self):
        self._data_dict = dict()
        for section, key_list in self.data.items():
            if section == "__meta__":
                continue

            self._data_dict[section] = dict()

            for key, params in key_list.items():
                self._data_dict[section][key] = {
                    'keys': params.get("keys", KeyError("required value")),
                    'default': params.get("default", None),
                    'action': params.get("action", 'store_const'),
                    'type': params.get("type", None),
                    'help': params.get("help", "Set {0} value".format(key)),
                    'validators': params.get("validators", (lambda x: x,)),
                    'metavar': params.get("metavar", key.upper())
                }

        # Add help text for groups

        # if defined
        if self.data.has_key('__meta__') and self.data["__meta__"].has_key('sections_help'):
            self._sections_help = self.data["__meta__"]["sections_help"]
        else:
            self._sections_help = {"sections_help": {}}

        for section in self.data.keys():
            if section == '__meta__':
                continue

            # Generate default if undefined
            self._sections_help[section] = self._sections_help.get(section, "{0} options".format(section.capitalize()))

    def options_builder(self):
        self.options_parser = OptionParser()
        self.options_parser.add_option(
            "--config", help="Set options from JSON file (generate example by --gen-conf).",
            action="callback", callback=self.load_config
        )

        for section, keys in self._data_dict.items():
            group = OptionGroup(title=self._sections_help[section], parser=self.options_parser)

            for dest, params in keys.items():
                group.add_option(*params['keys'],
                    action=params['action'],
                    dest=dest,
                    default=params['default'],
                    help=params['help'],
                    type=params['type'],
                    metavar=params['metavar']
                )

            self.options_parser.add_option_group(group)

        self.options_parser.add_option(
            "--gen-conf", help="Print sample config file and exit.",
            action="callback", callback=self.gen_conf
        )
        return self.options_parser

    def gen_conf(self, option, opt_str, value, parser, *args, **kwargs):
        config = dict()
        for section, params in self._data_dict.items():
            config[section] = dict()
            for key in params.keys():
                config[section][key] = parser.defaults.get(key, None)
        print(json.dumps(config, indent=1, default=lambda x: str(x)))
        exit(1)

    def load_config(self, option, opt_str, value, parser, *args, **kwargs):
        if not os.path.exists(opt_str):
            raise OptionValueError("Config file not exist")

        try:
            data = json.loads(codecs.open(value, "r", "utf-8"))
        except ValueError as e:
            raise OptionValueError("Config not valid JSON file\n\t{0}".format(str(e)))

        defaults = dict()

        for section, keys in data.items():
            for key, value in keys.items():
                if self.options_parser.defaults.has_key(key):
                    defaults[key] = value

        self.options_parser.defaults = defaults