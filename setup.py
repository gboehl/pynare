
# import  sys
# directory = '/home/gboehl/repos/pynare/'
# sys.path.append(directory)
# directory = '/home/gboehl/repos/matlab_wrapper3/'
# sys.path.append(directory)

from matlab_wrapper.matlab_session import MatlabSession
import warnings
from os import path
from setuptools import setup, find_packages

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
    install_requires=[],
)
