#!/bin/python3
# -*- coding: utf-8 -*-

import os
import sys


class PipeOutput(object):
    """A context manager that redirects stdout for its scope to a file, usage:

    with pipeOutput('log.txt'):
        os.system('ls -l')

    Attributes
    ----------
    logfile : str
        the full path to the output file
    stdout : object, optional
        the stdout object. Defaults to sys.stdout
    """

    def __init__(self, logfile, stdout=None):
        """
        Parameters
        ----------
        logfile : str
            the full path to the output file
        stdout : object, optional
            the stdout object. Defaults to sys.stdout
        """
        if stdout is None:
            stdout = sys.stdout

        stdout.flush()
        self._origstdout = stdout
        self._oldstdout_fno = os.dup(stdout.fileno())
        self._devnull = os.open(logfile, os.O_WRONLY)

    def __enter__(self):
        self._newstdout = os.dup(1)
        os.dup2(self._devnull, 1)
        os.close(self._devnull)
        sys.stdout = os.fdopen(self._newstdout, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._origstdout
        sys.stdout.flush()
        os.dup2(self._oldstdout_fno, 1)


def isnotebook():
    """A checker whether the code is running in an Jupyter notebook

    Returns
    -------
    bool
    """

    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except:
        return False      # Probably standard Python interpreter


def plot_eps(path, title):
    """Plots all '*.eps' files in folder

    Parameters
    ----------
    path : str
        the full path to the folder in which to look 
    title : str
        title string for the output plots
    """

    from PIL import Image
    import matplotlib.pyplot as plt

    figure = Image.open(path)
    # rescale it
    figure.load(scale=2)
    # create matplotlib figure in respective size
    fig = plt.figure(figsize=tuple([x/100 for x in figure.size]))
    ax = plt.axes([0, 0, 1, 1], frameon=False)
    plt.suptitle(title, fontsize=16, va='bottom', y=.02)
    plt.autoscale(tight=True)

    plt.imshow(figure)
    plt.ion()
    plt.show()


def print_progress(logfile):
    """Prints new lines arriving in logfile

    Parameters
    ----------
    logfile : str
        the full path to the logfile
    """

    import time

    f = open(logfile, 'r')
    p = 0

    while True:

        f.seek(p)
        latest_data = f.read()
        p = f.tell()

        if latest_data:
            sys.stdout.write(latest_data)
        else:
            time.sleep(1e-5)
