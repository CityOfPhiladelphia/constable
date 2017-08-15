#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name='constable',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'Flask-Cors==3.0.3',
        'gunicorn==19.7.1',
        'restful_ben==0.2.0'
    ],
    dependency_links=[
        'https://github.com/CityOfPhiladelphia/restful-ben/tarball/0.2.0#egg=restful_ben-0.2.0'
    ],
    entry_points={
        'console_scripts': [
            'constable=constable:main',
        ],
    }
)
