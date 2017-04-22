# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

pytest_plugins = "pytester",


def test_metadata(testdir):
    testdir.makepyfile("""
        def test_pass(metadata):
            for k in ['Python', 'Platform', 'Packages']:
                assert k in metadata
                assert 'JENKINS_URL' not in metadata
    """)
    result = testdir.runpytest()
    assert result.ret == 0


def test_environment_variables(testdir, monkeypatch):
    monkeypatch.setenv('JENKINS_URL', 'foo')
    monkeypatch.setenv('GIT_COMMIT', 'bar')
    testdir.makepyfile("""
        def test_pass(metadata):
            assert metadata.get('JENKINS_URL') == 'foo'
            assert metadata.get('GIT_COMMIT') == 'bar'
    """)
    result = testdir.runpytest()
    assert result.ret == 0


def test_additional_metadata(testdir):
    testdir.makepyfile("""
        def test_pass(metadata):
            assert metadata.get('Dave') == 'Hunt'
            assert metadata.get('Jim') == 'Bob'
    """)
    result = testdir.runpytest('--metadata', 'Dave', 'Hunt',
                               '--metadata', 'Jim', 'Bob')
    assert result.ret == 0
