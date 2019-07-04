#!/bin/python3
# -*- coding: utf-8 -*-

import sys
from pynare import pynare

if len(sys.argv) < 2:
    raise SyntaxError('No *.mod file provided!')

modpath = sys.argv[1]

mod0 = pynare(modpath)

