#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import copy
from collections import OrderedDict
from .fields import Field
from .exceptions import ValidationError


class DeclarativeFieldsMeta(type):

    def __new__(mcs, name, bases, attrs):
        current_fields = []
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                current_fields.append((key, value))
                attrs.pop(key)
        attrs['declared_fields'] = OrderedDict(current_fields)
        new_class = super().__new__(mcs, name, bases, attrs)

        declared_fields = OrderedDict()
        for base in reversed(new_class.__mro__):
            if hasattr(base, 'declared_fields'):
                declared_fields.update(base.declared_fields)

            for attr, value in base.__dict__.items():
                if value is None and attr in declared_fields:
                    declared_fields.pop(attr)

        new_class.base_fields = declared_fields
        new_class.declared_fields = declared_fields

        return new_class

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return OrderedDict()


class BaseForm(metaclass=DeclarativeFieldsMeta):

    def __init__(self, data=None):
        self.fields = copy.deepcopy(self.base_fields)
        self.data = {} if data is None else data
        self._errors = None
        self.valid_flag = None
        self._cleaned_data = OrderedDict()

    @property
    def cleaned_data(self):
        if self.valid_flag is None:
            raise ValidationError(msg="获得数据前，必须执行方法: is_valid")
        elif not self.valid_flag:
            raise ValidationError(msg="数据校验失败")
        else:
            return self._cleaned_data

    @property
    def errors(self):
        if self._errors is None:
            self.clean()
        return self._errors

    def value_from_datadict(self, data, name):
        return data.get(name)

    def clean(self):
        self.valid_flag = False
        cleaned_data = {}
        self._errors = {}
        for name, field in self.fields.items():
            value = self.value_from_datadict(self.data, name)
            try:
                value = field.clean(value)
                cleaned_data[name] = value
            except ValidationError as exc:
                self._errors[name] = exc.msg
        self.valid_flag = True
        self._cleaned_data = cleaned_data

    def is_valid(self):
        return self.data and not self.errors


class Form(BaseForm, metaclass=DeclarativeFieldsMeta):
    """表单实体"""

