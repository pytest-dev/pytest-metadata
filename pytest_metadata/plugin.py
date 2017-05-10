# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import platform

import _pytest._pluggy as pluggy
import pytest
import py

from pytest_metadata.ci import (
    appveyor, circleci, gitlab_ci, jenkins, taskcluster, travis_ci)


CONTINUOUS_INTEGRATION = {
    'AppVeyor': ['APPVEYOR', appveyor.ENVIRONMENT_VARIABLES],
    'CirceCI': ['CIRCLECI', circleci.ENVIRONMENT_VARIABLES],
    'GitLab CI': ['GITLAB_CI', gitlab_ci.ENVIRONMENT_VARIABLES],
    'Jenkins': ['JENKINS_URL', jenkins.ENVIRONMENT_VARIABLES],
    'TaskCluster': ['TASK_ID', taskcluster.ENVIRONMENT_VARIABLES],
    'Travis CI': ['TRAVIS', travis_ci.ENVIRONMENT_VARIABLES]}


@pytest.fixture(scope='session')
def metadata(pytestconfig):
    """Provide test session metadata"""
    return pytestconfig._metadata


def pytest_addoption(parser):
    parser.addoption('--metadata',
                     action='append',
                     default=[],
                     dest='metadata',
                     metavar=('key', 'value'),
                     nargs=2,
                     help='additional metadata.')


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config._metadata = {
        'Python': platform.python_version(),
        'Platform': platform.platform(),
        'Packages': {
            'pytest': pytest.__version__,
            'py': py.__version__,
            'pluggy': pluggy.__version__}}
    config._metadata.update({
        k: v for k, v in config.getoption('metadata')})

    plugins = dict()
    for plugin, dist in config.pluginmanager.list_plugin_distinfo():
        name, version = dist.project_name, dist.version
        if name.startswith('pytest-'):
            name = name[7:]
        plugins[name] = version
    config._metadata['Plugins'] = plugins

    for key, value in CONTINUOUS_INTEGRATION.items():
        [config._metadata.update({v: os.environ.get(v)})
            for v in value[1] if os.environ.get(v)]

    if hasattr(config, 'slaveoutput'):
        config.slaveoutput['metadata'] = config._metadata


def pytest_report_header(config):
    return 'metadata: {0}'.format(config._metadata)


@pytest.mark.optionalhook
def pytest_testnodedown(node):
    # note that any metadata from remote slaves will be replaced with the
    # environment from the final slave to quit
    if hasattr(node, 'slaveoutput'):
        node.config._metadata.update(node.slaveoutput['metadata'])
