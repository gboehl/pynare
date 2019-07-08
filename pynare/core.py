#!/bin/python3
# -*- coding: utf-8 -*-

import os
import shutil
import io
import sys
import tempfile
from .lib import PipeOutput, isnotebook, print_progress, plot_eps


class model(object):
    """The class holding information about the model and the engine.

    Attributes
    ----------
    modpath : str
        the full path to the *.mod-file
    engine : str, optional
        the engine. Must be either 'matlab' or 'octave'. None defaults to 'matlab'
    plot : bool, optional
        if True, loads all *.eps files from the model directory and displays them using matplotlib. Defaults to False if engine='matlab' and to True if engine='octave'
    verbose : bool, optional
        if True, prints the messages from dynare during calculation. Default is True

    Methods
    -------
    get_log()
        Prints the dynare log file for the provided model and returns it as a string
    run(verbose=None)
        Runs the model again
    """

    def __init__(self, modpath, engine=None, plot=None, verbose=True):
        """
        Parameters
        ----------
        modpath : str
            the full path to the *.mod-file
        engine : str, optional
            the engine. Must be either 'matlab' or 'octave'. None defaults to 'matlab'
        plot : bool, optional
            if True, loads all *.eps files from the model directory and displays them using matplotlib. Defaults to False if engine='matlab' and to True if engine='octave'
        verbose : bool, optional
            if True, prints the messages from dynare during calculation. Default is True

        Raises
        ------
        SyntaxError
            If provided file is not of '*.mod'-type
        NotImplementedError
            If engine is neither 'matlab' nor 'octave'
        """

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
                    "'engine' must either be 'matlab' (default) or 'octave'")
            try:
                import matlab.engine
                self.engine_type = 'matlab'
            except Exception as e:
                if engine == 'matlab':
                    raise
                else:
                    print(
                        '\nFailed to load matlab.engine. Falling back on octave engine. The following error was raised:\n', e)
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

                print("\nThe original octave plots do not work properly with oct2py. For that reason I am retrieving the stored *.eps figures from the dynare folder. This is somewhat old fasioned and does not allow for interactive figures.\n")

            from oct2py import octave

            self.eng = octave

        self.eng.eval('cd '+self.dirpath, nargout=0)

        if self.isnotebook and self.engine_type == 'matlab':
            print("Note: pynare is running in a Jupyter notebook or qtconsole. Both do not allow to (easily) redirect output from the matlab process to the interface. For that reason the '*.log' output will be blobbed just at the end of the calculation.\n")

        self.run()

    def __repr__(self):
        return "A DSGE Model for Dynare."

    @property
    def log(self):
        return self.get_log()

    def run(self, verbose=None):
        """Runs the model again

        Parameters
        ----------
        verbose : bool, optional
            if True, prints the messages from dynare during calculation. Default is True
        """

        if verbose is None:
            verbose = self.verbose

        # ensure that the logfile exists and that its empty
        blank = open(self.logfile, 'w')
        blank.close()

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
                if self.engine_type == 'octave':
                    self.imgs = self.eng.extract_figures(pltdir)
                    for img in self.imgs:
                        display(img)
                else:
                    print(
                        "'plot=True' not supported with matlab engine in Jupyter notebook.")

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

    def get_log(self):
        """Prints the dynare log file for the provided model and returns it as a string

        Returns
        -------
        str
            a string containting the text in the log file
        """

        open_lf = open(self.logfile, 'r')
        log_str = open_lf.read()
        sys.stdout.write(log_str)

        return log_str


def pynare(modpath=None, **kwargs):
    """The API to Pynare. Runs the model file and returns the Pynare model object.
    ...

    Parameters
    ----------
    modpath : str
        the full path to the *.mod-file
    engine : str, optional
        the engine. Must be either 'matlab' or 'octave'. None defaults to 'matlab'
    plot : bool, optional
        if True, loads all *.eps files from the model directory and displays them using matplotlib. Defaults to False if engine='matlab' and to True if engine='octave'
    verbose : bool, optional
        if True, prints the messages from dynare during calculation. Default is True

    Returns
    -------
    pynare.core.model
        the Pynare object containing the model

    Raises
    -------
    SyntaxError
        If provided file is not of '*.mod'-type
    """

    if modpath is None:
        if len(sys.argv) < 2:
            raise SyntaxError('No *.mod file provided!')

        modpath = sys.argv[1]
        need_pause = True
    else:
        need_pause = False

    mod_obj = model(modpath, **kwargs)

    if need_pause:
        input('\n[press Enter to exit]')
    else:
        return mod_obj
