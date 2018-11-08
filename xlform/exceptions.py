#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'


class ValidationError(Exception):
    """表单验证错误异常"""
    def __init__(self, *, code=None, msg=None):
        self.code = code
        self.msg = msg

    def __repr__(self):
        return '{}(code={}, msg={})'.format(self.__class__.__name__, self.code, self.msg)

