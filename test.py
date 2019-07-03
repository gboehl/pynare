#!/bin/python2
# -*- coding: utf-8 -*-

import os


class pynare(object):

    def __init__(self, modpath, engine='matlab', printout=None):

        self.modpath = modpath
        self.printout = printout

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

        self.run()

    ## this is a hack because the ipython notebook does not like to show terminal output
    def print_progress(self, logfile):

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
                print(latest_data)
                if 'Total computing time' in latest_data:
                    break
            else:
                time.sleep(.1)

    def run(self):

        if self.printout == 'notebook':

            from pathos.multiprocessing import ProcessPool
            pool = ProcessPool(nodes=2)

            fn = self.modpath[:-4]+'.log'

            pool.apipe(self.print_progress, fn)

        self.eng.eval('dynare '+os.path.basename(self.modpath)[:-4], nargout=0)

        self.workspace = self.eng.workspace
        self.oo_ = self.eng.workspace['oo_']


modpath = '/home/gboehl/rsh/bs18/dynare/SW_QE.mod'
pynare(modpath, printout='notebook')
