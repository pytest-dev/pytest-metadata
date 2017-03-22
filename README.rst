pytest-metadata
===============

pytest-metadata is a plugin for `pytest <http://pytest.org>`_ that provides
access to test session metadata.

.. image:: https://img.shields.io/badge/license-MPL%202.0-blue.svg
   :target: https://github.com/davehunt/pytest-metadata/blob/master/LICENSE
   :alt: License
.. image:: https://img.shields.io/pypi/v/pytest-metadata.svg
   :target: https://pypi.python.org/pypi/pytest-metadata/
   :alt: PyPI
.. image:: https://img.shields.io/travis/davehunt/pytest-metadata.svg
   :target: https://travis-ci.org/davehunt/pytest-metadata/
   :alt: Travis
.. image:: https://img.shields.io/github/issues-raw/davehunt/pytest-metadata.svg
   :target: https://github.com/davehunt/pytest-metadata/issues
   :alt: Issues
.. image:: https://img.shields.io/requires/github/davehunt/pytest-metadata.svg
   :target: https://requires.io/github/davehunt/pytest-metadata/requirements/?branch=master
   :alt: Requirements

Requirements
------------

You will need the following prerequisites in order to use pytest-metadata:

- Python 2.7, 3.6, PyPy, or PyPy3
- pytest 2.9.0 or newer

Installation
------------

To install pytest-metadata:

.. code-block:: bash

  $ pip install pytest-metadata

Available metadata
------------------

The following metadata is gathered by this plugin:

========  =============== ===================================
Key       Description     Example
========  =============== ===================================
Python    Python version  3.6.0
Platform  Platform        Darwin-16.4.0-x86_64-i386-64bit
Packages  pytest packages {'py': '1.4.33', 'pytest': '3.0.7'}
Plugins   pytest plugins  {'metadata': '1.3.0'}
========  =============== ===================================

Continuous integration
----------------------

When run in a continuous integration environment, additional metadata is added
from environment variables. Below is a list of the supported continuous
integration providers, along with links to the environment variables that are
added to metadata if they're present.

* `AppVeyor <https://www.appveyor.com/docs/environment-variables/>`_
* `CircleCI <https://circleci.com/docs/1.0/environment-variables/>`_
* `Jenkins <https://wiki.jenkins-ci.org/display/JENKINS/Building+a+software+project#Buildingasoftwareproject-JenkinsSetEnvironmentVariables>`_
* `TaskCluster <https://docs.taskcluster.net/reference/workers/docker-worker/environment>`_
* `Travis CI <https://docs.travis-ci.com/user/environment-variables/>`_

Note that if you're using `Tox <http://tox.readthedocs.io/>`_ to run your tests
then you will need to `pass down any additional environment variables <http://tox.readthedocs.io/en/latest/example/basic.html#passing-down-environment-variables>`_
for these to be picked up.

Accessing metadata
------------------

To access the metadata from a test or fixture, you can use the `metadata`
fixture:

.. code-block:: python

  def test_metadata(metadata):
      assert 'metadata' in metadata['Plugins']

To access the metadata from a plugin, you can use the `_metadata` attribute of
the `config` object. This can be used to read/add/modify the metadata:

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
