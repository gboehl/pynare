#!/bin/python2
# -*- coding: utf-8 -*-

from pynare import Pynare

modpath = '/home/gboehl/rsh/bs18/dynare/SW_QE.mod'

mod0 = Pynare(modpath)
mod0 = Pynare(modpath, engine='matlab')
mod0 = Pynare(modpath, engine='octave')

mod0.workspace
mod0.oo_['irfs']
# mod0.run()
# mod0.run(verbose=True)
