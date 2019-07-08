#!/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from pynare import pynare

modpath = '/home/gboehl/repos/pynare/tests/NK_IR04_rep.mod'

mod0 = pynare(modpath)
mod0 = pynare(modpath, engine='octave')

mod0.run()
logstr = mod0.get_log()
logstr

mod0.workspace
mod0.oo_['irfs']
fst_irf = list(mod0.oo_['irfs'].keys())[0]
irf_ml = mod0.oo_['irfs'][fst_irf]

irf = np.array(irf_ml).flatten()

plt.plot(irf)
