#!/bin/python2
# -*- coding: utf-8 -*-

import os
import sys


class PipeOutput(object):
    '''
    A context manager that redirects stdout for its scope, usage:

    with pipeOutput('log.txt'):
        os.system('ls -l')
    '''

    def __init__(self, logfile, stdout):
        stdout.flush()
        self._origstdout = stdout
        self._oldstdout_fno = os.dup(stdout.fileno())
        # self._devnull = os.open(os.devnull, os.O_WRONLY)
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

    import time

    blank = open(logfile, 'w')
    blank.close()

    f = open(logfile, 'r')
    p = 0

    while True:

        f.seek(p)
        latest_data = f.read()
        p = f.tell()

        if latest_data:
            sys.stdout.write(latest_data)
            # if 'Total computing time' in latest_data:
            # break
        else:
            time.sleep(1e-5)
