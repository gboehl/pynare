#!/bin/python3
# -*- coding: utf-8 -*-

import sys
from pynare import Pynare

if len(sys.argv) < 2:
    raise SyntaxError('No *.mod file provided!')

modpath = sys.argv[1]

try:
    mod0 = Pynare(modpath)
except:
    mod0 = Pynare(modpath, engine='octave')

input('\n[press Enter to exit]')
