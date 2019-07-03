#!/bin/python2
# -*- coding: utf-8 -*-

import os


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


class pynare(object):

    def __init__(self, modpath, engine='matlab'):

        self.modpath = modpath
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
            print("Note: pynare is running in a Jupyter notebook or  qtconsole. Both do not allow to (easily) redirect output from the matlab process to the interface. For that reason the '*.log' output will be blobbed at the end of the calculation, which may be incomplete.\n")

        self.run()

    def run(self):

        self.eng.eval('dynare '+os.path.basename(self.modpath)[:-4], nargout=0)

        self.workspace = self.eng.workspace
        self.oo_ = self.eng.workspace['oo_']

        if self.isnotebook:
            logfile = self.modpath[:-4] + '.log'
            lf = open(logfile, 'r')
            print(lf.read())
