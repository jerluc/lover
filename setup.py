#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='lover',
    version='0.1.0-alpha',
    description='A simple LOVE game development CLI',
    author='Jeremy Lucas',
    author_email='jeremyalucas@gmail.com',
    url='https://github.com/jerluc/lover',
    packages=['lover'],
    entry_points={
        'console_scripts': ['lover=lover.__main__:main'],
    },
    install_requires=[l.strip() for l in open('requirements.txt')],
    license='License :: OSI Approved :: Apache Software License',
)
