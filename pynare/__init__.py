#!/bin/python2
# -*- coding: utf-8 -*-

import os
import sys
import io


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


class pynare(object):

    def __init__(self, modpath, engine='matlab', verbose=True):

        self.modpath = modpath
        self.verbose = verbose
        self.lf = modpath[:-4] + '.log'
        self.isnotebook = isnotebook()

        if engine == 'matlab':

            import matlab.engine

            # the hack with a global seems necessary because matlab.engine.connect_matlab() does not work as expected and otherwise many engines would be initialized
            global mlengine

            if not 'mlengine' in globals():
                mlengine = matlab.engine.start_matlab()

            self.eng = mlengine

        elif engine == 'octave':

            from oct2py import octave

            self.eng = octave

        else:
            raise NotImplementedError(
                "'engine' must either be 'matlab' or 'octave'")

        if modpath[-4:] != '.mod':
            raise SyntaxError("mod-file must end with '*.mod'.")

        self.eng.eval('cd '+os.path.dirname(modpath), nargout=0)

        if self.isnotebook:
            print("Note: pynare is running in a Jupyter notebook or  qtconsole. Both do not allow to (easily) redirect output from the matlab process to the interface. For that reason the '*.log' output will be blobbed just at the end of the calculation.\n")

        self.run()

    def run(self, verbose=None):

        if verbose is None:
            verbose = self.verbose

        if verbose:
            if self.isnotebook:
                old_stdout = sys.stdout
                sys.stdout = io.TextIOWrapper(
                    open('/home/gboehl/lala'), encoding='UTF-8')
            else:
                from pathos.multiprocessing import ProcessPool
                pool = ProcessPool(nodes=2)
                pipe0 = pool.apipe(print_progress, self.lf)

        with PipeOutput(self.lf, sys.stdout):
            self.eng.eval(
                'dynare '+os.path.basename(self.modpath)[:-4], nargout=0)

        if verbose:
            if self.isnotebook:
                sys.stdout = old_stdout
                lf = open(self.lf, 'r')
                print(lf.read())
            else:
                pipe0

        self.workspace = self.eng.workspace
        self.oo_ = self.eng.workspace['oo_']
