
# import  sys
# directory = '/home/gboehl/repos/pynare/'
# sys.path.append(directory)
# directory = '/home/gboehl/repos/matlab_wrapper3/'
# sys.path.append(directory)

from os import path
# here = path.abspath(path.dirname(__file__))

from setuptools import setup, find_packages

print('Installing the matlab module...', end='')
from matlab_wrapper.matlab_session import MatlabSession

matlab = MatlabSession()
print('done.\n')

matlab.eval("cd (fullfile(matlabroot,'extern','engines','python'))")
matlab.eval("system('python setup.py install')")

setup(
        name = 'pynare',
        version = '0.1',
        author='Gregor Boehl',
        author_email='admin@gregorboehl.com',
        description='run DYNARE from python and access its workspace',
        packages = ['pynare'],
        install_requires=[],
   )
