#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import re
import uuid
from .exceptions import ValidationError


class BaseValidator:
    msg = 'value limit -> {}'

    def __init__(self, limit_value, msg=None):
        self.limit_value = limit_value
        if msg:
            self.msg = msg
        else:
            self.msg = self.msg.format(self.limit_value)

    def __call__(self, value):
        cleaned = self.clean(value)
        if self.compare(cleaned, self.limit_value):
            raise ValidationError(msg=self.msg)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.limit_value == other.limit_value and
            self.msg == other.msg
        )

    def compare(self, a, b):
        return a is not b

    def clean(self, x):
        return x


class MinLengthValidator(BaseValidator):
    msg = 'min_length -> {}'

    def compare(self, a, b):
        return a < b

    def clean(self, x):
        return len(x)


class MaxLengthValidator(BaseValidator):
    msg = 'max_length -> {}'

    def compare(self, a, b):
        return a > b

    def clean(self, x):
        return len(x)


class MinValueValidator(BaseValidator):
    msg = 'min_value -> {}'

    def compare(self, a, b):
        return a < b


class MaxValueValidator(BaseValidator):
    msg = 'max_value -> {}'

    def compare(self, a, b):
        return a > b


class DecimalValidator:
    msg = 'max_digits -> {}, max_decimal_places -> {}, max_whole_digits -> {}'

    def __init__(self, max_digits, decimal_places):
        self.max_digits = max_digits
        self.decimal_places = decimal_places

    def __call__(self, value):
        digit_tuple, exponent = value.as_tuple()[1:]
        if exponent >= 0:
            # A positive exponent adds that many trailing zeros.
            digits = len(digit_tuple) + exponent
            decimals = 0
        else:
            # If the absolute value of the negative exponent is larger than the
            # number of digits, then it's the same as the number of digits,
            # because it'll consume all of the digits in digit_tuple and then
            # add abs(exponent) - len(digit_tuple) leading zeros after the
            # decimal point.
            if abs(exponent) > len(digit_tuple):
                digits = decimals = abs(exponent)
            else:
                digits = len(digit_tuple)
                decimals = abs(exponent)
        whole_digits = digits - decimals

        if self.max_digits is not None and digits > self.max_digits:
            raise ValidationError(msg='max_digits -> {}'.format(self.max_digits))
        if self.decimal_places is not None and decimals > self.decimal_places:
            raise ValidationError(msg='max_decimal_places -> {}'.format(self.decimal_places))
        if (self.max_digits is not None and self.decimal_places is not None and
                whole_digits > (self.max_digits - self.decimal_places)):
            raise ValidationError(msg='max_whole_digits -> {}'.format(whole_digits))

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.max_digits == other.max_digits and
            self.decimal_places == other.decimal_places
        )


class RegexValidator:
    msg = "no match valid data"

    def __init__(self, regex, msg=None):
        self.regex = regex
        if msg:
            self.msg = msg

    def __call__(self, value):
        reg = self.regex
        if not reg.fullmatch(value):
            raise ValidationError(msg=self.msg)


class PhoneValidator:
    msg = "invalid phone"

    def __init__(self, msg=None):
        if msg:
            self.msg = msg

    def __call__(self, value):
        reg = re.compile(r'^1[3456789]\d{9}$')
        if not reg.fullmatch(value):
            raise ValidationError(msg=self.msg)


validate_phone = PhoneValidator()


class EmailValidator:
    msg = "invalid email"

    def __init__(self, msg=None):
        if msg:
            self.msg = msg

    def __call__(self, value):
        reg = re.compile(r'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$')
        if not reg.fullmatch(value):
            raise ValidationError(msg=self.msg)


validate_email = EmailValidator()


class UUIDValidator:
    msg = "invalid uuid value"

    def __init__(self, msg=None):
        if msg:
            self.msg = msg

    def __call__(self, value):
        if not isinstance(value, uuid.UUID):
            try:
                uuid.UUID(value)
            except ValueError:
                raise ValidationError(msg=self.msg)


validate_uuid = UUIDValidator()


class ProhibitNullCharactersValidator:
    """验证字符串不包含空字符"""
    msg = 'Null characters are not allowed.'

    def __init__(self, msg=None):
        if msg is not None:
            self.msg = msg

    def __call__(self, value):
        if '\x00' in str(value):
            raise ValidationError(msg=self.msg)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.msg == other.msg
        )




