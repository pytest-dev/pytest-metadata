# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import platform

import _pytest._pluggy as pluggy
import pytest
import py

from pytest_metadata.ci import (
    appveyor, circleci, jenkins, taskcluster, travis_ci)


CONTINUOUS_INTEGRATION = {
    'AppVeyor': ['APPVEYOR', appveyor.ENVIRONMENT_VARIABLES],
    'CirceCI': ['CIRCLECI', circleci.ENVIRONMENT_VARIABLES],
    'Jenkins': ['JENKINS_URL', jenkins.ENVIRONMENT_VARIABLES],
    'TaskCluster': ['TASK_ID', taskcluster.ENVIRONMENT_VARIABLES],
    'Travis CI': ['TRAVIS', travis_ci.ENVIRONMENT_VARIABLES]}


@pytest.fixture(scope='session')
def metadata(request):
    """Provide test session metadata"""
    return request.config._metadata


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    metadata = {
        'Python': platform.python_version(),
        'Platform': platform.platform(),
        'Packages': {
            'pytest': pytest.__version__,
            'py': py.__version__,
            'pluggy': pluggy.__version__}}

    plugins = dict()
    for plugin, dist in config.pluginmanager.list_plugin_distinfo():
        name, version = dist.project_name, dist.version
        if name.startswith('pytest-'):
            name = name[7:]
        plugins[name] = version
    metadata['Plugins'] = plugins

    for key, value in CONTINUOUS_INTEGRATION.items():
        [metadata.update({v: os.environ.get(v)})
            for v in value[1] if os.environ.get(v)]

    if hasattr(config, 'slaveoutput'):
        config.slaveoutput['metadata'] = metadata
    config._metadata = metadata


@pytest.mark.optionalhook
def pytest_testnodedown(node):
    # note that any metadata from remote slaves will be replaced with the
    # environment from the final slave to quit
    if hasattr(node, 'slaveoutput'):
        node.config._metadata = node.slaveoutput['metadata']
