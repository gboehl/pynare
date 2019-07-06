# pynare

This is a slim `Python` wrapper around `dynare`. It runs the `*.mod` file, displays the resulting output, and then provides access to the dynare workspace. It works with both, `Matlab` and `Octave`.

**NOTE:** This is at a very early stage and not well-tested (and not tested at all on Windows). You are very welcome to give comments via the [bug tracker](https://github.com/gboehl/pynare/issues). For now there is no live updating in the Jupyter Notebook, but information will be parsed after the calculation is finished. The reason is that it seems non-trivial to redirect printed matlab output (actual print output via `ctypes`) to Notebook cells while at the same time multiprocessing is not doing great in the Notebook.

For my fellow linux users, this also provieds a script to execute `dynare` from comand line.


## Motivation

The declared goal of this project is to provide access to `dynare` without having to learn and use `Matlab`/`Octave`. This reflects the acknowledgement that the translation of the `dynare` codebase to a more efficient open source alternative is a major effort which may take a while. Meanwhile, `pynare` encourages young researchers to focus on modern open source languages and, as the whole interface is pure `Python`, still allows them to use `dynare` without Matlab.


## Usage
Package import and running a modfile:
```
from pynare import Pynare
modfile = '/path/to/greatmodel.mod'
res = Pynare(modfile)
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

Just evoking `pynare` from the comand prompt/shell is as simple as
```
# pynare modelpath/crazy.mod
```


## Installation with `pip` (simple)

The simplest way is to [clone](https://github.com/gboehl/pynare/archive/master.zip) the repository, navigate to the cloned folder and run (Windows user from the Anaconda Prompt):
```
pip3 install .
```

## Installation with `pip` (elegant via `git`)

The handy way is to install via the `git`-command. If `git` is not yet installed, Linux users just use their respective repos, Windows users get it here: https://git-scm.com/download/win

```
pip3 install git+https://github.com/gboehl/pynare
```

Of course, installing `dynare` is your responibility.
