#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import re
import math
import copy
import itertools
from xlform import validators
from decimal import Decimal, DecimalException
from .exceptions import ValidationError


class Field:
    default_error_messages = {'required': 'This field is required'}
    default_validators = []
    empty_values = (None, '', [], (), {})

    def __init__(self, *, required=True, error_messages=None, validators=()):
        self.required = required
        messages = {}
        for c in reversed(self.__class__.__mro__):
            messages.update(getattr(c, 'default_error_messages', {}))
        if error_messages:
            messages['invalid'] = error_messages
        self.error_messages = messages
        self.validators = list(itertools.chain(self.default_validators, validators))

    def to_python(self, value):
        return value

    def validate(self, value):
        if value in self.empty_values and self.required:
            raise ValidationError(msg=self.error_messages['required'])

    def run_validators(self, value):
        if value in self.empty_values:
            return
        errors = []
        for v in self.validators:
            try:
                v(value)
            except ValidationError as exc:
                errors.append(exc.msg)
        if errors:
            raise ValidationError(msg=', '.join(errors))

    def clean(self, value):
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        return value

    def __deepcopy__(self, memo):
        result = copy.copy(self)
        memo[id(self)] = result
        result.validators = self.validators[:]
        return result


class CharField(Field):

    def __init__(self, *, max_length=None, min_length=None, strip=False, empty_value=None, **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        self.strip = strip
        self.empty_value = empty_value
        super().__init__(**kwargs)
        if min_length is not None:
            self.validators.append(validators.MinLengthValidator(int(min_length)))
        if max_length is not None:
            self.validators.append(validators.MaxLengthValidator(int(max_length)))
        self.validators.append(validators.ProhibitNullCharactersValidator())

    def to_python(self, value):
        if value not in self.empty_values:
            value = str(value)
            if self.strip:
                value = value.strip()
        else:
            return self.empty_value
        return value


class PhoneField(CharField):
    default_validators = [validators.validate_phone]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class EmailField(CharField):
    default_validators = [validators.validate_email]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RegexField(CharField):

    def __init__(self, regex, **kwargs):
        """
        regex can be either a string or a compiled regular expression object.
        """
        kwargs.setdefault('strip', False)
        super().__init__(**kwargs)
        self._set_regex(regex)

    @property
    def regex(self):
        return self._regex

    def _set_regex(self, regex):
        if isinstance(regex, str):
            regex = re.compile(regex)
        self._regex = regex
        self._regex_validator = validators.RegexValidator(regex=regex)
        self.validators.append(self._regex_validator)


class UUIDField(CharField):
    default_validators = [validators.validate_uuid]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class BooleanField(Field):

    def to_python(self, value):
        if isinstance(value, str) and value.lower() in ('false', '0'):
            value = False
        else:
            value = bool(value)
        return super().to_python(value)


class NullBooleanField(BooleanField):

    def to_python(self, value):
        if value in (True, 'True', 'true', '1'):
            return True
        elif value in (False, 'False', 'false', '0'):
            return False
        else:
            return None


class IntegerField(Field):
    default_error_messages = {
        'invalid': 'Enter a whole number'
    }
    re_decimal = re.compile(r'\.0*\s*$')

    def __init__(self, *, max_value=None, min_value=None, **kwargs):
        self.max_value, self.min_value = max_value, min_value
        super().__init__(**kwargs)

        if max_value is not None:
            self.validators.append(validators.MaxValueValidator(max_value))
        if min_value is not None:
            self.validators.append(validators.MinValueValidator(min_value))

    def to_python(self, value):
        if value in self.empty_values:
            return
        try:
            value = int(self.re_decimal.sub('', str(value)))
        except (ValueError, TypeError):
            raise ValidationError(msg=self.error_messages['invalid'])
        return value


class FloatField(IntegerField):
    default_error_messages = {
        'invalid': 'Enter a number',
    }

    def to_python(self, value):
        value = super(IntegerField, self).to_python(value)
        if value in self.empty_values:
            return
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise ValidationError(msg=self.error_messages['invalid'])
        return value

    def validate(self, value):
        super().validate(value)
        if value in self.empty_values:
            return
        if not math.isfinite(value):
            raise ValidationError(msg=self.error_messages['invalid'])


class DecimalField(IntegerField):
    default_error_messages = {
        'invalid': 'Enter a Decimal value',
    }

    def __init__(self, *, max_value=None, min_value=None, max_digits=None, decimal_places=None, **kwargs):
        """
        :param max_value: 最大数值
        :param min_value: 最小数值
        :param max_digits: 数字允许的最大位数, 如果存在decimal_places, 此数字必须是大于decimal_places
        :param decimal_places: 小数位数

        eg:
            例如，要存储的数字最大长度为3位，而带有两个小数位，可以使用：max_digits=3, decimal_places=2
        """
        self.max_digits, self.decimal_places = max_digits, decimal_places
        super().__init__(max_value=max_value, min_value=min_value, **kwargs)
        self.validators.append(validators.DecimalValidator(max_digits, decimal_places))

    def to_python(self, value):
        if value in self.empty_values:
            return
        value = str(value).strip()
        try:
            value = Decimal(value)
        except DecimalException:
            raise ValidationError(msg=self.error_messages['invalid'])
        return value

    def validate(self, value):
        super().validate(value)
        if value in self.empty_values:
            return
        if not math.isfinite(value):
            raise ValidationError(msg=self.error_messages['invalid'])






