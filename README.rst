pytest-metadata
===============

pytest-metadata is a plugin for `pytest <http://pytest.org>`_ that provides
access to test session metadata.

.. image:: https://img.shields.io/badge/license-MPL%202.0-blue.svg
   :target: https://github.com/pytest-dev/pytest-metadata/blob/master/LICENSE
   :alt: License
.. image:: https://img.shields.io/pypi/v/pytest-metadata.svg
   :target: https://pypi.python.org/pypi/pytest-metadata/
   :alt: PyPI
.. image:: https://img.shields.io/travis/pytest-dev/pytest-metadata.svg
   :target: https://travis-ci.org/pytest-dev/pytest-metadata/
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Travis
.. image:: https://img.shields.io/github/issues-raw/pytest-dev/pytest-metadata.svg
   :target: https://github.com/pytest-dev/pytest-metadata/issues
   :alt: Issues
.. image:: https://img.shields.io/requires/github/pytest-dev/pytest-metadata.svg
   :target: https://requires.io/github/pytest-dev/pytest-metadata/requirements/?branch=master
   :alt: Requirements

Requirements
------------

You will need the following prerequisites in order to use pytest-metadata:

- Python 2.7, 3.6, PyPy, or PyPy3

Installation
------------

To install pytest-metadata:

.. code-block:: bash

  $ pip install pytest-metadata

Development
-----------

To contribute to pytest-metadata it helps to
have `Pipenv <https://pipenv.readthedocs.io/en/latest/>`_
and `pre-commit <https://pre-commit.com/>`_ installed.

.. code-block:: bash

  $ pipenv install --dev
  $ pre-commit install

Running Tests
_____________

We use `Tox <http://tox.testrun.org/>`_ to manage running tests
against the supported Python versions.

.. code-block:: bash

  $ pipenv run tox

Available metadata
------------------

The following metadata is gathered by this plugin:

========  =============== ===================================
Key       Description     Example
========  =============== ===================================
Python    Python version  3.6.4
Platform  Platform        Darwin-17.4.0-x86_64-i386-64bit
Packages  pytest packages {'py': '1.5.2', 'pytest': '3.4.1'}
Plugins   pytest plugins  {'metadata': '1.6.0'}
========  =============== ===================================

Additional metadata
-------------------

You can provide your own metadata (key, value pair) by specifying ``--metadata`` on the commandline::

   pytest --metadata foo bar

Note: You can provide multiple sets of ``--metadata``::

   pytest --metadata foo bar --metadata baz zoo

Continuous integration
----------------------

When run in a continuous integration environment, additional metadata is added
from environment variables. Below is a list of the supported continuous
integration providers, along with links to the environment variables that are
added to metadata if they're present.

* `AppVeyor <https://www.appveyor.com/docs/environment-variables/>`_
* `CircleCI <https://circleci.com/docs/1.0/environment-variables/>`_
* `GitLab CI <http://docs.gitlab.com/ce/ci/variables/README.html>`_
* `Jenkins <https://wiki.jenkins-ci.org/display/JENKINS/Building+a+software+project#Buildingasoftwareproject-JenkinsSetEnvironmentVariables>`_
* `TaskCluster <https://docs.taskcluster.net/reference/workers/docker-worker/environment>`_
* `Travis CI <https://docs.travis-ci.com/user/environment-variables/>`_

Note that if you're using `Tox <http://tox.readthedocs.io/>`_ to run your tests
then you will need to `pass down any additional environment variables <http://tox.readthedocs.io/en/latest/example/basic.html#passing-down-environment-variables>`_
for these to be picked up.

Viewing metadata
----------------

If you pass ``--verbose`` on the command line when running your tests, then the
metadata will be displayed in the terminal report header::

  pytest --verbose
  ============================ test session starts ============================
  platform darwin -- Python 3.6.4, pytest-3.4.1, py-1.5.2, pluggy-0.6.0 -- /usr/bin/python
  cachedir: .pytest_cache
  metadata: {'Python': '3.6.4', 'Platform': 'Darwin-17.4.0-x86_64-i386-64bit', 'Packages': {'pytest': '3.4.1', 'py': '1.5.2', 'pluggy': '0.6.0'}, 'Plugins': {'metadata': '1.6.0'}}
  plugins: metadata-1.6.0

Accessing metadata
------------------

To add/modify/delete metadata at the end of metadata collection, you can use the ``pytest_metadata`` hook:

.. code-block:: python

  import pytest
  @pytest.mark.optionalhook
  def pytest_metadata(metadata):
      for key in metadata.keys():
         if "password" in key.lower():
            del metadata[key]

To access the metadata from a test or fixture, you can use the ``metadata``
fixture:

.. code-block:: python

  def test_metadata(metadata):
      assert 'metadata' in metadata['Plugins']

To access the metadata from a plugin, you can use the ``_metadata`` attribute of
the ``config`` object. This can be used to read/add/modify the metadata:

.. code-block:: python

  def pytest_configure(config):
    if hasattr(config, '_metadata'):
        config._metadata['foo'] = 'bar'

Plugin integrations
-------------------

Here's a handy list of plugins that either read or contribute to the metadata:

* `pytest-base-url <https://pypi.python.org/pypi/pytest-base-url/>`_ - Adds the
  base URL to the metadata.
* `pytest-html <https://pypi.python.org/pypi/pytest-html/>`_ - Displays the
  metadata at the start of each report.
* `pytest-selenium <https://pypi.python.org/pypi/pytest-selenium/>`_ - Adds the
  driver, capabilities, and remote server to the metadata.

Resources
---------

- `Release Notes <http://github.com/davehunt/pytest-metadata/blob/master/CHANGES.rst>`_
- `Issue Tracker <http://github.com/davehunt/pytest-metadata/issues>`_
- `Code <http://github.com/davehunt/pytest-metadata/>`_
