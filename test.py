#!/bin/python2
# -*- coding: utf-8 -*-

from pynare import pynare

modpath = '/home/gboehl/rsh/bs18/dynare/SW_QE.mod'

mod0 = pynare(modpath)
# mod0 = pynare(modpath, verbose=False)

# mod0.workspace
# mod0.oo_['irfs']
mod0.run()
mod0.run(verbose=True)
