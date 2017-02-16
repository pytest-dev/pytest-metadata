# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import platform

import _pytest._pluggy as pluggy
import pytest
import py


ENV = [
    # Jenkins
    'BUILD_NUMBER',
    'BUILD_ID',
    'BUILD_URL',
    'NODE_NAME',
    'JOB_NAME',
    'BUILD_TAG',
    'EXECUTOR_NUMBER',
    'JENKINS_URL',
    'JAVA_HOME',
    'WORKSPACE',
    'SVN_REVISION',
    'CVS_BRANCH',
    'GIT_COMMIT',
    'GIT_URL',
    'GIT_BRANCH',
    # Travis
    'CI',
    'CONTINUOUS_INTEGRATION',
    'TRAVIS',
    'TRAVIS_BRANCH',
    'TRAVIS_BUILD_ID',
    'TRAVIS_BUILD_NUMBER',
    'TRAVIS_COMMIT',
    'TRAVIS_COMMIT_MESSAGE',
    'TRAVIS_COMMIT_RANGE',
    'TRAVIS_EVENT_TYPE',
    'TRAVIS_JOB_ID',
    'TRAVIS_JOB_NUMBER',
    'TRAVIS_OS_NAME',
    'TRAVIS_PULL_REQUEST',
    'TRAVIS_PULL_REQUEST_BRANCH',
    'TRAVIS_PULL_REQUEST_SHA',
    'TRAVIS_PULL_REQUEST_SLUG',
    'TRAVIS_REPO_SLUG',
    'TRAVIS_SUDO',
    'TRAVIS_TAG',
    # TaskCluster
    'TASK_ID',
    'RUN_ID',
]


@pytest.fixture(scope='session')
def metadata(request):
    """Provide test session metadata"""
    return request.config._metadata


def pytest_configure(config):
    metadata = {
        'Python': platform.python_version(),
        'Platform': platform.platform(),
        'pytest': pytest.__version__,
        'py': py.__version__,
        'pluggy': pluggy.__version__}

    plugins = []
    for plugin, dist in config.pluginmanager.list_plugin_distinfo():
        name = '{0.project_name}-{0.version}'.format(dist)
        if name.startswith('pytest-'):
            name = name[7:]
        plugins.append(name)
    metadata['Plugins'] = list(set(plugins))

    [metadata.update({v: os.environ.get(v)}) for v in ENV if os.environ.get(v)]
    if hasattr(config, 'slaveoutput'):
        config.slaveoutput['metadata'] = metadata
    config._metadata = metadata


@pytest.mark.optionalhook
def pytest_testnodedown(node):
    # note that any metadata from remote slaves will be replaced with the
    # environment from the final slave to quit
    if hasattr(node, 'slaveoutput'):
        node.config._metadata = node.slaveoutput['metadata']
