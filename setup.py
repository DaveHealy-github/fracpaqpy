# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='fracpaq',
    version='0.1.0',
    description='fracpaqpy is based on the MATLAB version of FracPaQ, written by Dave Healy, Roberto Rizzo, and others.',
    long_description=readme,
    author='Dave Healy',
    author_email='',
    url='https://github.com/koan-analytics/fracpaqpy',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
