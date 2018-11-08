#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'junxi'

import xlform
from setuptools import setup, find_packages

setup(
    name="xlform",
    version=xlform.__version__,
    author="junxi",
    author_email="xinlei3166@126.com",
    description="一个仿 django form 的表单验证库",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    url="https://github.com/xinlei3166/xlform",
    license="BSD License",
    platforms='any',
    packages=['xlform'],
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=True,
    # install_requires=[
    #     'Django>=1.10,<=2.1',
    # ],
)


