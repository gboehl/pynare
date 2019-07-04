#!/bin/python2
# -*- coding: utf-8 -*-

from pynare import pynare

modpath = '/home/gboehl/rsh/bs18/dynare/SW_QE.mod'
# modpath = $1

mod0 = pynare(modpath)

# mod0.workspace
# mod0.oo_['irfs']
mod0.run()
