#!/bin/python2
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from pynare import Pynare
from pynare import pynare

modpath = '/home/gboehl/repos/pynare/tests/NK_IR04_rep.mod'

# mod0 = Pynare(modpath)
mod0 = Pynare(modpath, engine='octave')

mod0 = pynare(modpath)
mod0 = pynare(modpath, engine='octave')

# mod0.run()

mod0.workspace
mod0.oo_['irfs']
mod0.oo_['irfs'].keys()
irf_ml = mod0.oo_['irfs']['y_epsa_']

irf = np.array(irf_ml).flatten()

plt.plot(irf)
