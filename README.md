# pynare

This is a slim Python wrapper around **Dynare**. It runs the mod file and then provides access to the workspace.

**NOTE:** This is at a very early stage and not well-tested (and not tested at all on Windows). You are very welcome to give comments via the bug reports.


Usage:
```
from pynare import pynare
modfile = '\home\cooluser\greatmodel.mod'
res = pynare(modfile)
```

This will give you the usual info about how the Blanchard-Kahn conditions are messed up. Then access the attributes:
```
res.workspace                   # will give you the matlab workspace
print(res.workspace['beta'])    # it contains all the parameters
>>> 0.995                       # likely to be the case
```

I also added the 'oo_' matlab-dynare object, which contains a lot of usefull stuff. Note that you could have also accessed it via `res.workspace['oo_']`.
```
res.oo_.keys()              # it is a dict, so browse it via `keys()`
irfs = res.oo_['irfs']      # for instance get your impulse response functions (it's again a dict). Maybe plot them?
```


## Installation with `pip` (simple)

The simplest way is to clone the repository and then from within the cloned folder run (Windows user from the Anaconda Prompt):
```
pip3 install .
```

## Installation with `pip` (elegant via `git`)

The handy way is to first install `git`. Linux users just use their respective repos. Windows users get it here: https://git-scm.com/download/win

```
pip3 install git+https://github.com/gboehl/pynare
```
