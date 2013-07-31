#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* Created by PyCharm.
* Date: 29.07.13
* Time: 23:09
* Original filename: 
"""

__author__ = 'mosquito'

class ValidationError(Exception): pass

class ValidatorBase(object):
    def __init__(self, *args, **kwargs):
        self.critical = kwargs.get('critical', False)
        self.args = args
        self.kwargs = kwargs

    def __call__(self, arg, options=None, parser=None, dest=None, *args):
        try:
            self.arg = arg
            self.options = options
            self.name = dest
            self.parser = parser
            self.call()
        except ValidationError as e:
            raise ValidationError(e)
        except Exception as e:
            raise Exception(e)

    def call(self):
        pass

class ValidationQueue(ValidatorBase):
    def call(self):
        for func in self.args:
            if isinstance(func, ValidatorBase):
                func(arg=self.arg, options=self.options, parser=self.parser, dest=self.name)

class ValidOnce(ValidatorBase):
    def call(self):
        res = True
        for func in self.args:
            res = res or func(self.arg)
            if res:
                return res

        if not res:
            raise ValidationError("ValidOnce validation error")
        else:
            return res

class ValidAll(ValidatorBase):
    def call(self):
        res = True
        for func in self.args:
            res = res and func(self.arg)

        if not res:
            raise ValidationError("Value \"{0}\" for option \"{1}\" not valid".format(self.arg, self.name))
        else:
            return res

class RequireAll(ValidatorBase):
    def call(self):
        res = dict()

        for arg in self.args:
            try:
                res[arg] = True and getattr(self.options, arg)
            except AttributeError as e:
                res[arg] = False

        nores = dict(filter(lambda v: True and v[1], res.items())).keys()
        if nores:
            raise ValidationError("\"{0}\": this option requires the ads the following options: [{1}]".format(self.name, ", ".join(nores)))

class RequireOnce(ValidatorBase):
    def call(self):
        res = dict()

        for arg in self.args:
            try:
                res[arg] = True and getattr(self.options, arg)
            except AttributeError as e:
                res[arg] = False

        nores = dict(filter(lambda v: True and v[1], res.items())).keys()
        if not nores:
            raise ValidationError("\"{0}\", this option requires the ads one of the options: [{1}]".format(self.name, ", ".join(nores)))

class Conflict(ValidatorBase):
    def call(self):
        res = dict()

        for arg in self.args:
            try:
                res[arg] = True and getattr(self.options, arg)
            except AttributeError as e:
                res[arg] = False

        nores = dict(filter(lambda v: bool(v[1]), res.items())).keys()
        if nores:
            raise ValidationError("\"{0}\", this option conflicts with the following options: [{1}]".format(self.name, ", ".join(nores)))

# Synonyms
Valid = ValidAll
Require = RequireAll