**pynare**
==========

This is a slim Python API to Dynare. It runs the ``*.mod`` file, displays the resulting output, and then provides access to the Dynare workspace. It works with both, Matlab and Octave.

For fellow linux users (and probably mac users as well), this also provides a script to execute Dynare from comand line.

- Source: https://github.com/gboehl/pynare
- Documentation: https://pynare.readthedocs.io/en/latest/
- Bug tracker: https://github.com/gboehl/pynare/issues

**NOTE:** This is at a very early stage and not well-tested (and not tested at all on Windows). Comments via the `bug tracker <https://github.com/gboehl/pynare/issues>`_ are very welcome. 

Motivation
----------

The declared goal of this project is to provide access to Dynare without having to learn and use Matlab / Octave. This reflects the acknowledgement that the translation of the Dynare codebase to a more efficient open source alternative is a major effort which may take a while. Meanwhile, **pynare** encourages young researchers to focus on modern open source languages and, as the whole interface is pure Python, still allows them to use Dynare without Matlab.


Usage
-----

Package import and running a modfile:

.. code-block:: python

   from pynare import Pynare
   modfile = '/path/to/greatmodel.mod'
   res = Pynare(modfile)

This will give you the usual info about how the Blanchard-Kahn conditions are messed up. Then access the attributes:

.. code-block:: python

   res.workspace                   # will give you the matlab workspace
   print(res.workspace['beta'])    # it contains all the parameters
   >>> 0.995                       # likely to be the case

I also added the ``oo_`` Dynare-object, which contains a lot of usefull stuff. Note that you could have also accessed it via ``res.workspace['oo_']``.

.. code-block:: python

   res.oo_.keys()              # it is a dict, so browse it via `keys()`
   irfs = res.oo_['irfs']      # for instance get your impulse response functions (it's again a dict). Maybe plot them?

Just evoking **pynare** from the comand prompt/shell is as simple as

.. code-block:: sh

  pynare modelpath/crazy.mod

Installation with ``pip`` (simple)
--------------------------------------

The simplest way is to `clone <https://github.com/gboehl/pynare/archive/master.zip>`_ the repository, navigate to the cloned folder and run (Windows user from the Anaconda Prompt):

.. code-block:: sh

   pip3 install .

Installation with ``pip`` (elegant via ``git``\ )
-------------------------------------------------------

The handy way is to install via the ``git``\ -command. If ``git`` is not yet installed, Linux users just use their respective repos, Windows users get it here: https://git-scm.com/download/win

.. code-block:: sh

   pip3 install git+https://github.com/gboehl/pynare

Of course, installing Dynare remains your responibility.
