
# import  sys
# directory = '/home/gboehl/repos/pynare/'
# sys.path.append(directory)
# directory = '/home/gboehl/repos/matlab_wrapper3/'
# sys.path.append(directory)

from os import path
here = path.abspath(path.dirname(__file__))
print(here)

from setuptools import setup, find_packages
from matlab_wrapper.matlab_session import MatlabSession

print('installing the matlab module...')
matlab = MatlabSession()

matlab.eval("cd (fullfile(matlabroot,'extern','engines','python'))")
matlab.eval("system('python setup.py install')")
print('installing the actual package...')

setup(
        name = 'pynare',
        version = 'alpha',
        author='Gregor Boehl',
        author_email='admin@gregorboehl.com',
        description='run DYNARE from python and access its workspace',
        # packages = find_packages(),
        packages = ['pynare'],
        install_requires=[],
   )
