#!/usr/bin/env python

import os
import platform
import sys
import warnings

try:
    import setuptools
    from setuptools import setup
except ImportError:
    setuptools = None
    from distutils.core import setup

from nanoservice.version import VERSION


with open('README.md') as fh:
    long_description = fh.read()

setup(
    name='nanoservice',
    version=VERSION,
    packages = ['nanoservice'],
    author='Tony Walker',
    author_email='walkr.walkr@gmail.com',
    url='https://github.com/walkr/nanoservice',
    license='MIT',
    description='nanoservice is a small Python library for writing lightweight networked services using nanomsg',
    long_description=long_description,
    install_requires=[
        'msgpack-python',
        'nanomsg',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        ],
)