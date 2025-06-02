# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import json
import os
import platform
from typing import Dict, Callable

from pytest import PytestPluginManager, Config, Parser

try:
    import _pytest._pluggy as pluggy
except ImportError:
    import pluggy
import pytest

from pytest_metadata.ci import (
    appveyor,
    bitbucket,
    circleci,
    codebuild,
    gitlab_ci,
    jenkins,
    taskcluster,
    travis_ci,
)

CONTINUOUS_INTEGRATION = [
    appveyor.ENVIRONMENT_VARIABLES,
    bitbucket.ENVIRONMENT_VARIABLES,
    circleci.ENVIRONMENT_VARIABLES,
    codebuild.ENVIRONMENT_VARIABLES,
    gitlab_ci.ENVIRONMENT_VARIABLES,
    jenkins.ENVIRONMENT_VARIABLES,
    taskcluster.ENVIRONMENT_VARIABLES,
    travis_ci.ENVIRONMENT_VARIABLES,
]

metadata_key = pytest.StashKey[dict]()


def pytest_addhooks(pluginmanager: PytestPluginManager) -> None:
    from pytest_metadata import hooks

    pluginmanager.add_hookspecs(hooks)


@pytest.fixture(scope="session")
def metadata(pytestconfig: Config) -> Dict:
    """Provide test session metadata"""
    return pytestconfig.stash[metadata_key]


@pytest.fixture(scope="session")
def include_metadata_in_junit_xml(
    metadata: Dict,
    pytestconfig: Config,
    record_testsuite_property: Callable[[str, object], None],
) -> None:
    """Provide test session metadata"""
    metadata_ = pytestconfig.stash[metadata_key]
    for name, value in metadata_.items():
        record_testsuite_property(name, value)


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("pytest-metadata")
    group.addoption(
        "--metadata",
        action="append",
        default=[],
        dest="metadata",
        metavar=("key", "value"),
        nargs=2,
        help="additional metadata.",
    )
    group.addoption(
        "--metadata-from-json",
        action="store",
        default="{}",
        dest="metadata_from_json",
        help="additional metadata from a json string.",
    )
    group.addoption(
        "--metadata-from-json-file",
        type=str,
        dest="metadata_from_json_file",
        help="additional metadata from a json file.",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: Config) -> None:
    config.stash[metadata_key] = {
        "Python": platform.python_version(),
        "Platform": platform.platform(),
        "Packages": {
            "pytest": pytest.__version__,
            "pluggy": pluggy.__version__,
        },
    }
    config.stash[metadata_key].update({k: v for k, v in config.getoption("metadata")})
    config.stash[metadata_key].update(
        json.loads(config.getoption("metadata_from_json"))
    )

    if config.getoption("metadata_from_json_file"):
        with open(config.getoption("metadata_from_json_file"), "r") as json_file:
            config.stash[metadata_key].update(json.load(json_file))
    plugins = dict()
    for plugin, dist in config.pluginmanager.list_plugin_distinfo():
        name, version = dist.project_name, dist.version
        if name.startswith("pytest-"):
            name = name[7:]
        plugins[name] = version
    config.stash[metadata_key]["Plugins"] = plugins

    for provider in CONTINUOUS_INTEGRATION:
        for var in provider:
            if os.environ.get(var):
                config.stash[metadata_key].update({var: os.environ.get(var)})

    if hasattr(config, "workeroutput"):
        config.workeroutput["metadata"] = config.stash[metadata_key]
    config.hook.pytest_metadata(metadata=config.stash[metadata_key], config=config)


def pytest_report_header(config: Config) -> str | None:
    if config.getoption("verbose") > 0:
        return "metadata: {0}".format(config.stash[metadata_key])


@pytest.hookimpl(optionalhook=True)
def pytest_testnodedown(
    node: "pytest_xdist.WorkerController",  # noqa: F821
) -> None:  # type:ignore[name-defined]
    # note that any metadata from remote workers will be replaced with the
    # environment from the final worker to quit
    if hasattr(node, "workeroutput"):
        node.config.stash[metadata_key].update(node.workeroutput["metadata"])
