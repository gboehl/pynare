#!/bin/python2
# -*- coding: utf-8 -*-

import os

class pynare(object):

    def __init__(self, modpath, engine='matlab'):

        self.modpath = modpath

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
            raise NotImplementedError("'engine' must either be 'matlab' or 'octave'")

        if modpath[-4:] != '.mod':
            raise SyntaxError("mod-file must end with '*.mod'.")

        self.eng.eval('cd '+os.path.dirname(modpath), nargout=0)
        self.eng.eval('dynare '+os.path.basename(modpath)[:-4], nargout=0)

        self.workspace = self.eng.workspace
        self.oo_ = self.eng.workspace['oo_']


    def run(self):

        self.eng.eval('dynare '+os.path.basename(self.modpath)[:-4], nargout=0)

        self.workspace = self.eng.workspace
        self.oo_ = self.eng.workspace['oo_']

modpath = '/home/gboehl/rsh/bs18/dynare/SW_QE.mod'
mod0 = pynare(modpath)
mod0.workspace.__dir__()
mod0.workspace['beta']
mod0.oo_['irfs'].

"""
import oct2py, os
from oct2py import octave
octave.eval('cd '+os.path.dirname(modpath))
octave.eval('dynare '+os.path.basename(modpath)[:-4])

## something wrong here
octave.register_graphics_toolkit('gtk3')
octave.register_graphics_toolkit('gnuplot')
octave.register_graphics_toolkit('qt')
octave.graphics_toolkit('qt')
octave.graphics_toolkit('gtk3')
octave.graphics_toolkit('gnuplot')
octave.available_graphics_toolkits()
"""

