# -*- coding: utf-8 -*-

import pytest


pytestmark = pytest.mark.usefixtures('black_available')


def test_help_message(testdir):
    result = testdir.runpytest("--help")
    result.stdout.fnmatch_lines(["*--black*enable format checking with black"])


def test_fail(testdir):
    """Assert test fails due to single quoted strings
    """
    testdir.makepyfile(
        """
        def hello():
            print('Hello, world')
    """
    )
    result = testdir.runpytest("--black")
    result.assert_outcomes(failed=1)


def test_pass(testdir):
    """Assert test passes when no formatting issues are found
    """
    p = testdir.makepyfile(
        """
        def hello():
            print("Hello, world!")
    """
    )
    # replace trailing newline (stripped by testdir.makepyfile)
    p = p.write(p.read() + "\n")

    result = testdir.runpytest("--black")
    result.assert_outcomes(passed=1)


def test_mtime_cache(testdir):
    """Assert test is skipped when file hasn't changed
    """
    p = testdir.makepyfile(
        """
        def hello():
            print("Hello, world!")
    """
    )
    # replace trailing newline (stripped by testdir.makepyfile)
    contents = p.read() + "\n"
    p.write(contents)

    # Test once to populate the cache
    result = testdir.runpytest("--black")
    result.assert_outcomes(passed=1)

    # Run it again, it should be skipped
    result = testdir.runpytest("--black", "-rs")
    result.assert_outcomes(skipped=1)
    result.stdout.fnmatch_lines(["SKIP*previously passed black format checks"])

    # Update the file and test again.
    p.write(contents)
    result = testdir.runpytest("--black")
    result.assert_outcomes(passed=1)


def test_exclude(testdir):
    """Assert test is skipped if path is excluded even if also included
    """
    testdir.makefile(
        "pyproject.toml",
        """
        [tool.black]
            include = 'test_exclude.py'
            exclude = '.*'
    """,
    )
    p = testdir.makepyfile(
        """
        def hello():
            print("Hello, world!")
    """
    )

    # replace trailing newline (stripped by testdir.makepyfile)
    p = p.write(p.read() + "\n")

    # Rename pyproject.toml ¯\_(ツ)_/¯
    testdir.run("mv", "test_exclude.pyproject.toml", "pyproject.toml")

    result = testdir.runpytest("--black")
    result.assert_outcomes(skipped=1, passed=0)


def test_include(testdir):
    """Assert test is not skipped if path is included but not excluded
    """
    testdir.makefile(
        "pyproject.toml",
        """
        [tool.black]
            include = 'test_include'
    """,
    )
    p = testdir.makepyfile(
        """
        def hello():
            print("Hello, world!")
    """
    )

    # replace trailing newline (stripped by testdir.makepyfile)
    p = p.write(p.read() + "\n")

    # Rename pyproject.toml ¯\_(ツ)_/¯
    testdir.run("mv", "test_include.pyproject.toml", "pyproject.toml")

    result = testdir.runpytest("--black")
    result.assert_outcomes(skipped=0, passed=1)


def test_pytest_deprecation_warning(testdir):
    """Assert no deprecation warning is raised during test."""
    p = testdir.makepyfile(
        """
        def hello():
            print("Hello, world!")
    """
    )
    # replace trailing newline (stripped by testdir.makepyfile)
    p = p.write(p.read() + "\n")

    result = testdir.runpytest("--black")
    result.assert_outcomes(passed=1)

    out = "\n".join(result.stdout.lines)
    assert "PytestUnknownMarkWarning" not in out
