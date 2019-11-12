
Q-CTRL Qiskit
=============

The aim of the Q-CTRL Qiskit package is to provide export functions allowing
users to deploy established error-robust quantum control protocols from the
open literature and defined in Q-CTRL Open Controls on IBM Quantum hardware.

Anyone interested in quantum control is welcome to contribute to this project.

Table of Contents
-----------------


* `Installation <#installation>`_
* `Usage <#usage>`_
* `Contributing <#contributing>`_
* `Credits <#credits>`_
* `License <#license>`_

Installation
------------

Q-CTRL Qiskit can be install through ``pip`` or from source. We recommend
the ``pip`` distribution to get the most recent stable release. If you want the
latest features then install from source.

Requirements
^^^^^^^^^^^^

To use Q-CTRL Qiskit you will need an installation of Python. We
recommend using the `Anaconda <https://www.anaconda.com/>`_ distribution of
Python. Anaconda includes standard numerical and scientific Python packages
which are optimally compiled for your machine. Follow the `Anaconda
Installation <https://docs.anaconda.com/anaconda/install/>`_ instructions and
consult the `Anaconda User
guide <https://docs.anaconda.com/anaconda/user-guide/>`_ to get started.

We use interactive jupyter notebooks for our usage examples. The Anaconda
python distribution comes with editors for these files, or you can `install the
jupyter notebook editor <https://jupyter.org/install>`_ on its own.

Using PyPi
^^^^^^^^^^

Use ``pip`` to install the latest version of Q-CTRL Qiskit.

.. code-block:: shell

   pip install qctrl-qiskit

From Source
^^^^^^^^^^^

The source code is hosted on
`Github <https://github.com/qctrl/python-qiskit>`_. The repository can be
cloned using

.. code-block:: shell

   git clone git@github.com:qctrl/python-qiskit.git

Once the clone is complete, you have two options:


#. 
   Using setup.py

   .. code-block:: shell

      cd python-qiskit
      python setup.py develop

   **Note:** We recommend installing using ``develop`` to point your installation
   at the source code in the directory where you cloned the repository.

#. 
   Using Poetry

   .. code-block:: shell

      cd python-qiskit
      ./setup-poetry.sh

   **Note:** if you are on Windows, you'll need to install
   `Poetry <https://poetry.eustace.io>`_ manually, and use:

   .. code-block:: bash

      cd python-qiskit
      poetry install

Once installed via one of the above methods, test your installation by running
``pytest``
in the ``python-qiskit`` directory.

.. code-block:: shell

   pytest

Usage
-----

See the `Jupyter notebooks <https://github.com/qctrl/notebooks/tree/master/qctrl-open-controls>`_.

Contributing
------------

For general guidelines, see `Contributing <https://github.com/qctrl/.github/blob/master/CONTRIBUTING.md>`_.

Building documentation
^^^^^^^^^^^^^^^^^^^^^^

Documentation generation relies on `Spinx <http://www.sphinx-doc.org>`_. Automated builds are done by `Read The Docs <https://readthedocs.com>`_.

To build locally:


#. Ensure you have used one of the install options above.
#. 
   Execute the make file from the docs directory:

    If using Poetry:

   .. code-block:: bash

       cd docs
       poetry run make html

    If using setuptools:

   .. code-block:: bash

       cd docs
       # Activate your virtual environment if required
       make html

The generated HTML will appear in the ``docs/_build/html`` directory.

Credits
-------

See
`Contributors <https://github.com/qctrl/python-qiskit/graphs/contributors>`_.

License
-------

See `LICENSE <LICENSE>`_.
