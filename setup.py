#!/bin/python3
# -*- coding: utf-8 -*-

from matlab_wrapper.matlab_session import MatlabSession
import warnings
from os import path
from setuptools import setup, find_packages

try:
    import matlab.engine
    print('matlab engine already installed.\n')
except:
    print('Installing the matlab engine...', end='')
    try:
        matlab = MatlabSession()

        matlab.eval("cd (fullfile(matlabroot,'extern','engines','python'))")
        matlab.eval("system('python setup.py install')")

        try:
            import matlab.engine
            print('done.\n')
        except:
            warnings.warn(
                "\nFailed to install matlab engine. In any case you can use pynare with engine='octave'.\n")

    except:
        warnings.warn(
            "\nFailed to access matlab installation. Is it installed? In any case you can use pynare with engine='octave'.\n")

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://pynare.readthedocs.io/en/latest/index.html",
    name='pynare',
    version='0.1.5',
    author='Gregor Boehl',
    author_email='admin@gregorboehl.com',
    license='MIT',
    description='run DYNARE from python and access its workspace',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=['pynare'],
    entry_points={
          'console_scripts': [
              'pynare = pynare.core:pynare'
          ]
    },
    install_requires=['numpy', 
                      'pathos'],
    include_package_data=True,
)
