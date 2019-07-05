#!/bin/python2
# -*- coding: utf-8 -*-

import os
import shutil
import io
import sys
import tempfile
from .lib import PipeOutput, isnotebook, print_progress, plot_eps


class Pynare(object):

    def __init__(self, modpath, engine=None, plot=None, verbose=True):

        if modpath[-4:] != '.mod':
            raise SyntaxError("mod-file must be of '*.mod'-type.")

        self.modpath = modpath
        self.modname = os.path.basename(modpath)[:-4]
        self.dirpath = os.path.dirname(modpath)
        self.logfile = modpath[:-4] + '.log'

        self.verbose = verbose
        self.isnotebook = isnotebook()

        if engine != 'octave':
            if engine is not None and not 'matlag':
                raise NotImplementedError(
                    "'engine' must either be 'matlab'(default) or 'octave'")
            try:
                import matlab.engine
                self.engine_type = 'matlab'
            except Exception as e:
                if engine == 'matlab':
                    raise e
                else:
                    print(
                        'Failed to load matlab.engine. Falling back on octave engine. The following error was raised: ', e)
                    self.engine_type = 'octave'
        else:
            self.engine_type = 'octave'

        if self.engine_type == 'matlab':

            if plot is None:
                self.plot = False

            # the hack with a global seems necessary because matlab.engine.connect_matlab() does not work as expected and otherwise many engines would be initialized
            global mlengine

            if not 'mlengine' in globals():
                mlengine = matlab.engine.start_matlab()

            self.eng = mlengine

        else:

            if plot is None:

                self.plot = True

                print("The original octave plots do not work properly with oct2py. For that reason I'm retrieving the stored *.eps figures from the dynare folder. This is somewhat old fasioned and does not allow for interactive figures.\n")

            from oct2py import octave

            self.eng = octave

        self.eng.eval('cd '+self.dirpath, nargout=0)

        if self.isnotebook and self.engine_type == 'matlab':
            print("Note: pynare is running in a Jupyter notebook or qtconsole. Both do not allow to (easily) redirect output from the matlab process to the interface. For that reason the '*.log' output will be blobbed just at the end of the calculation.\n")

        self.run()

    def run(self, verbose=None):

        if verbose is None:
            verbose = self.verbose

        if verbose:
            if self.isnotebook:
                old_stdout = sys.stdout
                sys.stdout = tempfile.TemporaryFile()
            else:
                from pathos.multiprocessing import ProcessPool
                pool = ProcessPool(nodes=2)
                pipe0 = pool.apipe(print_progress, self.logfile)

        if self.engine_type == 'matlab':

            with PipeOutput(self.logfile, sys.stdout):
                self.eng.eval('dynare '+self.modname, nargout=0)

            self.workspace = self.eng.workspace
            self.oo_ = self.eng.workspace['oo_']

        else:

            # need to dump the original octave plots somewhere
            pltdir = os.path.join(tempfile.gettempdir(), 'plt')
            if not os.path.isdir(pltdir):
                os.mkdir(pltdir)

            with PipeOutput(self.logfile, sys.stdout):
                self.eng.feval('dynare', self.modname, plot_dir=pltdir)

            oct_ws_list = self.eng.eval('who', nout=1)
            self.workspace = {var: self.eng.pull(var) for var in oct_ws_list}
            self.oo_ = self.workspace['oo_']

        if self.plot:

            if self.isnotebook:
                self.imgs = self.eng.extract_figures(pltdir)
                for img in self.imgs:
                    display(img)

            else:
                epsfiles = [f for f in os.listdir(self.dirpath) if '.eps' in f]

                for figname in epsfiles:
                    figpath = os.path.join(self.dirpath, figname)
                    figtitle = figname.replace(
                        self.modname+'_', '').replace('.eps', '')
                    plot_eps(figpath, figtitle)

        if self.engine_type == 'octave':
            shutil.rmtree(pltdir)

        if verbose:
            if self.isnotebook:
                sys.stdout = old_stdout
                if self.engine_type == 'matlab':
                    lf = open(self.logfile, 'r')
                    sys.stdout.write(lf.read())
            else:
                pipe0
