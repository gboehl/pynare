**pynare**
==========

This is a slim Python wrapper to Dynare. It runs the ``*.mod`` file, displays the resulting output, and then provides access to the Dynare workspace. It works with both, Matlab and Octave.

For fellow linux users (and probably mac users as well), this also provides a script to execute Dynare from comand line.

- Source: https://github.com/gboehl/pynare
- Documentation: https://pynare.readthedocs.io/en/latest/
- Bug tracker: https://github.com/gboehl/pynare/issues

**NOTE:** Since my other packages have sufficiently matured, I do not have to use dynare anymore. This means that this is no longer under active development! Check out my `econpizza <https://github.com/gboehl/econpizza>`_ package for the solution and simulation of nonlinear DSGE models (with or without heterogeneous agents).   

Comments via the `bug tracker <https://github.com/gboehl/pynare/issues>`_ are still welcome. 

Motivation
----------

The declared goal of this project is to provide access to Dynare without having to learn and use Matlab/Octave. This reflects the acknowledgement that the translation of the Dynare codebase to a more efficient open source alternative is a major effort which may take a while. Meanwhile, **pynare** encourages young researchers to focus on modern open source languages and, as the whole interface is pure Python, still allows them to use Dynare without Matlab.


Usage
-----

I assume that you have dynare installed and added to your octave/matlab path permanently.
Package import and running a modfile:

.. code-block:: python

   from pynare import pynare, set_dynare_path
   set_dynare_path('/path/to/dynare')   # e.g. /usr/lib/dynare/matlab/
   modfile = '/path/to/greatmodel.mod'
   mod0 = pynare(modfile)

This will give you the usual info about how the Blanchard-Kahn conditions are messed up. The ``mod0``-object contains all the stuff from dynare. Access the attributes with:

.. code-block:: python

   mod0.workspace                   # will give you the matlab workspace
   print(mod0.workspace['beta'])    # it contains all the parameters
   >>> 0.995                       # likely to be the case

I also added the ``oo_`` Dynare-object, which contains a lot of usefull stuff. Note that you could have also accessed it via ``mod.workspace['oo_']``.

.. code-block:: python

   mod0.oo_.keys()              # it is a dict, so browse it via `keys()`
   irfs = mod0.oo_['irfs']      # for instance get your impulse response functions (it's again a dict). Maybe plot them?

Just evoking **pynare** from the comand prompt/shell is as simple as

.. code-block:: sh

  pynare modelpath/crazy.mod

Installation via ``pip``
--------------------------------------

Installation is as simply as running (Windows users from the Anaconda Prompt):

.. code-block:: sh

   pip install pynare

Of course, installing Dynare remains your responibility. Also, be sure that dynare is added to your octave/matlab path.

If you care for the bleeding edge developing version (which, at this stage, is recommended), the handy way is to install via the ``git``-command. If you hav not yet installed ``git``, Windows users get it here: https://git-scm.com/download/win (Linux users just use the repo of their distro). Then:

.. code-block:: sh

   pip install git+https://github.com/gboehl/pynare
