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
        'marshmallow==2.13.5',
        'psycopg2==2.7.1',
        'requests==2.18.4',
        'restful_ben==0.3.0',
        'zxcvbn-python==4.4.16'
    ],
    dependency_links=[
        'https://github.com/CityOfPhiladelphia/restful-ben/tarball/0.3.0#egg=restful_ben-0.3.0'
    ],
    entry_points={
        'console_scripts': [
            'constable=constable:main',
        ],
    }
)
