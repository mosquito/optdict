#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* Date: 29.07.13
* Time: 0:12
* Original filename: 
"""

from __future__ import print_function, absolute_import
from optparse import OptionParser, OptionGroup, OptionValueError, OptionConflictError
import sys
import codecs
import json
from optdict import validators
import os

__author__ = 'mosquito'

class Parser(object):
    def __init__(self, dictionary):
        assert isinstance(dictionary, dict)
        self.__data = dictionary
        self.__validators = dict()
        self._validate_dict()

    def __str__(self):
        return json.dumps((self._data_dict, self._sections_help), indent=1, default=lambda n: str(n))

    def _key(self, section, key):
        return "{0}_{1}".format(section, key)

    def _validate_dict(self):
        self._data_dict = dict()
        for section, key_list in self.__data.items():
            if section == "__meta__":
                continue

            self._data_dict[section] = dict()

            for key, params in key_list.items():
                full_key = self._key(section, key)
                self._data_dict[section][key] = {
                    'keys': params.get("keys", None),
                    'default': params.get("default", None),
                    'dest': full_key,
                    'action': params.get("action", "store"),
                    'type': params.get("type", None),
                    'help': str(params.get("help", "Set {0} value".format(key))),
                    'validator': params.get("validator", validators.Valid(lambda x: True,)),
                    'metavar': params.get("metavar", key.upper())
                }
                option = self._data_dict[section][key]

                if option['action'].startswith("store") and \
                        option['type'] == None:
                    option['type'] = "string"

                if option['action'].startswith("store") and not option["default"] == None:
                    option["help"] = "{0} [Default: {1}]".format(option['help'], option['default'])

                if option['keys'] == None:
                    raise OptionValueError("required value")

                if option['action'] == "store_true" and \
                    option['default'] == None:
                    option.pop('type')
                    option['default'] = False

                if option['action'] == "store_false" and \
                    option['default'] == None:
                    option.pop('type')
                    option['default'] = True

                if option['action'] == "store_const":
                    option.pop('type')

                if "count" in option['action']:
                    option.pop('type')

                if option['action'] == 'callback':
                    if not option['type']:
                        option.pop('type')

                    option.pop('default')
                    option['callback'] = params.get("callback", None)

                    if option['callback'] == None:
                        raise OptionValueError("required value")


        # Add help text for groups

        # if defined
        if self.__data.has_key('__meta__'):
            self._sections_help = self.__data["__meta__"].get("sections_help", {"sections_help": {}})
            self._sections_descriptions = self.__data["__meta__"].get("sections_text", {"sections_text": {}})

            self.__usage = self.__data['__meta__'].get("usage", None)

        for section in self.__data.keys():
            if section == '__meta__': continue
            # Generate default if undefined
            self._sections_help[section] = self._sections_help.get(section, "{0} options".format(section.capitalize()))

        for section in self.__data.keys():
            if section == '__meta__': continue
            # Generate default if undefined
            self._sections_descriptions[section] = self._sections_descriptions.get(section, None)

    def _options_builder(self):
        self._options_parser = OptionParser()
        self._options_parser.add_option(
            "--config", help="Set options from JSON file (generate example by --gen-conf).",
            action="callback", type="string", callback=self._load_config, metavar="file".upper()
        )

        for section, keys in self._data_dict.items():
            group = OptionGroup(
                title=self._sections_help[section],
                parser=self._options_parser,
                description=self._sections_descriptions[section]
            )

            for key, params in keys.items():
                self.__validators[self._key(section, key)] = params.pop("validator")
                group.add_option(*params.pop('keys'), **params)

            self._options_parser.add_option_group(group)

        self._options_parser.add_option(
            "--gen-conf", "--gen-config", help="Print sample config file and exit.",
            action="callback", callback=self._gen_conf
        )
        return self._options_parser

    def _gen_conf(self, option, opt_str, value, parser, *args, **kwargs):
        config = dict()
        for section, params in self._data_dict.items():
            config[section] = dict()
            for key in params.keys():
                config[section][key] = parser.defaults.get("{0}_{1}".format(section, key), None)
        print(json.dumps(config, indent=1, default=lambda x: str(x)))
        exit(1)

    def _load_config(self, option, opt_str, value, parser, *args, **kwargs):
        if not os.path.exists(value):
            raise OptionValueError("Config file not exist")

        try:
            data = json.loads(codecs.open(value, "r", "utf-8").read())
        except (ValueError, TypeError) as e:
            raise OptionValueError("Config not valid JSON file\n\t{0}".format(str(e)))

        for section, keys in data.items():
            for key, value in keys.items():
                dest = self._key(section, key)
                if self._options_parser.defaults.has_key(dest):
                    setattr(parser.values, dest, value)

        parser.values.config = data

    def _validate(self, options, args):
        for dest, func in self.__validators.items():
            if func:
                try:
                    value = getattr(options, dest)

                    if isinstance(func, validators.ValidatorBase):
                        func(arg=value, options=options, parser=self._options_parser, dest=dest)
                    else:
                        raise validators.ValidationError("Validator must be instance ValidationBase")
                except validators.ValidationError as e:
                    sys.stderr.write("{2}\n ERROR: Validator for key \"{0}\" error:\n{1}\n{2}\n".format(dest, str(e), "=" * 50))
                    sys.stderr.flush()
                except Exception as e:
                    raise e

                if func.critical:
                    exit(128)

    def _to_dict(self):
        out = dict([(section, {}) for section in self._data_dict.keys()])
        for key, value in self.parser.values.__dict__.items():
            for section in out.keys():
                if key.startswith(section):
                    out[section][key.replace("{0}_".format(section), "")] = value

        return out

    def parse_args(self):
        self.parser = self._options_builder()
        options, args = self.parser.parse_args()
        self._validate(options, args)
        options.to_dict = lambda : self._to_dict()
        return (options, args)