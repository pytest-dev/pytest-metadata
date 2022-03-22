# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import pytest
from xml.etree import ElementTree as ET
from tempfile import NamedTemporaryFile

pytest_plugins = ("pytester",)


def test_metadata(testdir):
    testdir.makepyfile(
        """
        def test_pass(metadata):
            for k in ['Python', 'Platform', 'Packages']:
                assert k in metadata
                assert 'JENKINS_URL' not in metadata
    """
    )
    result = testdir.runpytest()
    assert result.ret == 0


def test_environment_variables(testdir, monkeypatch):
    monkeypatch.setenv("JENKINS_URL", "foo")
    monkeypatch.setenv("GIT_COMMIT", "bar")
    testdir.makepyfile(
        """
        def test_pass(metadata):
            assert metadata.get('JENKINS_URL') == 'foo'
            assert metadata.get('GIT_COMMIT') == 'bar'
    """
    )
    result = testdir.runpytest()
    assert result.ret == 0


def test_additional_metadata(testdir):
    testdir.makepyfile(
        """
        def test_pass(metadata):
            assert metadata.get('Dave') == 'Hunt'
            assert metadata.get('Jim') == 'Bob'
    """
    )
    result = testdir.runpytest("--metadata", "Dave", "Hunt", "--metadata", "Jim", "Bob")
    assert result.ret == 0


@pytest.mark.parametrize("junit_format", ["xunit1", "xunit2"])
def test_junit_integration(testdir, junit_format):
    testdir.makepyfile(
        """
        import pytest

        pytestmark = pytest.mark.usefixtures('include_metadata_in_junit_xml')

        def test_pass():
            pass
    """
    )
    result = testdir.runpytest(
        "--metadata",
        "Daffy",
        "Duck",
        "--junit-xml=results.xml",
        "--override-ini='junit_family={}'".format(junit_format),
    )
    assert result.ret == 0
    results_file = testdir.tmpdir.join("results.xml")
    assert results_file.exists()
    with results_file.open() as fd:
        xml = ET.parse(fd)
    properties = xml.findall(".//property")
    xml_metadata = [p.attrib for p in properties]
    # value passed on the cmdline appears
    assert {"name": "Daffy", "value": "Duck"} in xml_metadata


def test_additional_metadata_from_json(testdir):
    testdir.makepyfile(
        """
        def test_pass(metadata):
            assert metadata.get('Imran') == 'Mumtaz'
    """
    )
    result = testdir.runpytest("--metadata-from-json", '{"Imran": "Mumtaz"}')
    assert result.ret == 0


def test_additional_metadata_from_json_file(testdir):
    testdir.makepyfile(
        """
        def test_pass(metadata):
            assert metadata.get('John') == 'Cena'
    """
    )

    json_temp = NamedTemporaryFile(delete=False)
    json_temp.write('{"John": "Cena"}'.encode(encoding="utf-8"))
    json_temp.flush()
    result = testdir.runpytest("--metadata-from-json-file", json_temp.name)
    assert result.ret == 0


def test_additional_metadata_using_key_values_json_str_and_file(testdir):
    testdir.makepyfile(
        """
        def test_pass(metadata):
            assert metadata.get('John') == 'Cena'
            assert metadata.get('Dwayne') == 'Johnson'
            assert metadata.get('Andre') == 'The Giant'
    """
    )
    json_temp = NamedTemporaryFile(delete=False)
    json_temp.write('{"Andre": "The Giant"}'.encode(encoding="utf-8"))
    json_temp.flush()
    result = testdir.runpytest(
        "--metadata",
        "John",
        "Cena",
        "--metadata-from-json",
        '{"Dwayne": "Johnson"}',
        "--metadata-from-json-file",
        json_temp.name,
    )
    assert result.ret == 0


def test_metadata_hook(testdir):
    testdir.makeconftest(
        """
        import pytest
        @pytest.mark.optionalhook
        def pytest_metadata(metadata):
            metadata['Dave'] = 'Hunt'
    """
    )
    testdir.makepyfile(
        """
        def test_pass(metadata):
            assert metadata.get('Dave') == 'Hunt'
    """
    )
    result = testdir.runpytest()
    assert result.ret == 0


def test_report_header(testdir):
    result = testdir.runpytest()
    assert not any(line.startswith("metadata:") for line in result.stdout.lines)
    result = testdir.runpytest("-v")
    assert any(line.startswith("metadata:") for line in result.stdout.lines)
