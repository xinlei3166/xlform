#!/usr/bin/env python
# _*_ coding:utf-8 _*_

"""一个仿 django form 的表单验证库

Usages:

    from xlform.forms import Form
    from xlform.fields import *


    class NF(Form):
        a = CharField(max_length=4, min_length=2, empty_value='123')
        b = CharField(max_length=4, min_length=2, required=False, empty_value='222')
        phone = PhoneField(max_length=11)
        email = EmailField()
        reg = RegexField(regex='^1[3456789]\d{9}$')
        uuid = UUIDField(required=False)
        boolean = BooleanField(required=False)
        integer = IntegerField(max_value=11)
        ft = FloatField(max_value=12)
        dc = DecimalField(max_digits=3, decimal_places=1, required=False)


    data = {
        # 'a': '12',
        'b': '123',
        'phone': '16666666666',
        'email': '16666666666@qq.com',
        'reg': '16666666666',
        'uuid': '998a281c-e257-11e8-b428-8c85904e5604',
        'boolean': 0,
        'integer': '11',
        'ft': '11.1111',
        'dc': 11.0
    }

    nf = NF(data)
    if nf.is_valid():
        print(nf.cleaned_data)
    else:
        print(nf.errors)
"""

__author__ = 'junxi'
__version__ = '0.1.4'

from xlform.forms import Form
from xlform.fields import *

__all__ = [
    'Form',
    'Field',
    'CharField',
    'PhoneField',
    'EmailField',
    'RegexField',
    'UUIDField',
    'BooleanField',
    'IntegerField',
    'FloatField',
    'DecimalField',
    'ValidationError'
]


