#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name='constable',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'Flask-Cors==3.0.3',
        'restful_ben==0.0.2'
    ],
    dependency_links=[
        'https://github.com/CityOfPhiladelphia/restful-ben/tarball/0.0.2#egg=restful_ben-0.0.2'
    ],
)
