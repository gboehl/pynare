# pynare

This is a slim `Python` wrapper around **`Dynare`**. It runs the `*.mod` file and then provides access to the dynare workspace. 

**NOTE:** This is at a very early stage and not well-tested (and not tested at all on Windows). You are very welcome to give comments via the [bug tracker](https://github.com/gboehl/pynare/issues). For now this does not work well in the Jupyter Notebook. The reason is that it seems non-trivial to redirect printed matlab output to Notebook cells. Hints are appreciated.


## Motivation
The declared (long time) goal of this project is to provide access to **`Dynare`** without having to learn and use `Matlab`/`Octave`. This reflects the acknowledgement that the translation of the **`Dynare`** codebase to a moder open-source alternative requires a major effort and can not be expected any time soon. In the same time we want young researchers to focuss on modern open-source languages and unburden them from having to learn `Matlab`. With **`pynare`** it is no longer necessary to touch `Matlab` as the whole interface is pure `Python`.


Usage:
```
from pynare import pynare
modfile = '/path/to/greatmodel.mod'
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

The simplest way is to [clone](https://github.com/gboehl/pynare/archive/master.zip) the repository, navigate to the cloned folder and run (Windows user from the Anaconda Prompt):
```
pip3 install .
```

## Installation with `pip` (elegant via `git`)

The handy way is to first install `git`. Linux users just use their respective repos, Windows users get it here: https://git-scm.com/download/win

```
pip3 install git+https://github.com/gboehl/pynare
```
