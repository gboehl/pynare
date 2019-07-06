#!/bin/python2
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


setup(
    name='pynare',
    version='0.1',
    author='Gregor Boehl',
    author_email='admin@gregorboehl.com',
    description='run DYNARE from python and access its workspace',
    packages=['pynare'],
    # scripts=['run_pynare.py'],
    # scripts=['pynare.py'],
    # scripts=['pynare:.py'],
    entry_points={
          'console_scripts': [
              'pynare = pynare.core:run'
          ]
    },
    install_requires=['numpy', 
                      'pathos'],
)
