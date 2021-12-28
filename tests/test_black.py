# -*- coding: utf-8 -*-

import pytest


pytestmark = pytest.mark.usefixtures('black_available')


def test_help_message(pytester):
    result = pytester.runpytest("--help")
    result.stdout.fnmatch_lines(["*--black*enable format checking with black"])


def test_fail(pytester):
    """Assert test fails due to single quoted strings
    """
    pytester.makepyfile(
        """
        def hello():
            print('Hello, world')
    """
    )
    result = pytester.runpytest("--black")
    result.assert_outcomes(failed=1)


def test_pass(pytester):
    """Assert test passes when no formatting issues are found
    """
    p = pytester.makepyfile(
        """
        def hello():
            print("Hello, world!")
    """
    )
    # replace trailing newline (stripped by pytester.makepyfile)
    p = p.write_text(p.read_text() + "\n")

    result = pytester.runpytest("--black")
    result.assert_outcomes(passed=1)


def test_mtime_cache(pytester):
    """Assert test is skipped when file hasn't changed
    """
    p = pytester.makepyfile(
        """
        def hello():
            print("Hello, world!")
    """
    )
    # replace trailing newline (stripped by pytester.makepyfile)
    contents = p.read_text() + "\n"
    p.write_text(contents)

    # Test once to populate the cache
    result = pytester.runpytest("--black")
    result.assert_outcomes(passed=1)

    # Run it again, it should be skipped
    result = pytester.runpytest("--black", "-rs")
    result.assert_outcomes(skipped=1)
    result.stdout.fnmatch_lines(["SKIP*previously passed black format checks"])

    # Update the file and test again.
    p.write_text(contents)
    result = pytester.runpytest("--black")
    result.assert_outcomes(passed=1)


def test_exclude(pytester):
    """Assert test is skipped if path is excluded even if also included
    """
    pytester.makepyprojecttoml(
        """
        [tool.black]
            include = 'test_exclude.py'
            exclude = '.*'
    """,
    )
    p = pytester.makepyfile(
        """
        def hello():
            print("Hello, world!")
    """
    )

    # replace trailing newline (stripped by pytester.makepyfile)
    p = p.write_text(p.read_text() + "\n")

    # Rename pyproject.toml ¯\_(ツ)_/¯
    pytester.run("mv", "test_exclude.pyproject.toml", "pyproject.toml")

    result = pytester.runpytest("--black")
    result.assert_outcomes(skipped=1, passed=0)


def test_exclude_folder(pytester):
    """Assert test is skipped for files in a folder
    """
    pytester.makepyprojecttoml(
        """
        [tool.black]
            exclude = '''
            (
              /(
                  first_folder
                | ignore_folder
              )/
            )
    '''
    """,
    )
    p = pytester.makepyfile(
        """
        def hello():
            print("Hello, world!")
    """
    )
    # replace trailing newline (stripped by pytester.makepyfile)
    p = p.write_text(p.read_text() + "\n")

    # Move file into folder that should be excluded
    ignore_folder = pytester.mkdir("ignore_folder")
    pytester.run("mv", "test_exclude_folder.py", ignore_folder)

    # Rename pyproject.toml ¯\_(ツ)_/¯
    pytester.run("mv", "test_exclude_folder.pyproject.toml", "pyproject.toml")

    result = pytester.runpytest("--black")
    result.assert_outcomes(skipped=1, passed=0)


def test_include(pytester):
    """Assert test is not skipped if path is included but not excluded
    """
    pytester.makepyprojecttoml(
        """
        [tool.black]
            include = 'test_include'
    """,
    )
    p = pytester.makepyfile(
        """
        def hello():
            print("Hello, world!")
    """
    )

    # replace trailing newline (stripped by pytester.makepyfile)
    p = p.write_text(p.read_text() + "\n")

    # Rename pyproject.toml ¯\_(ツ)_/¯
    pytester.run("mv", "test_include.pyproject.toml", "pyproject.toml")

    result = pytester.runpytest("--black")
    result.assert_outcomes(skipped=0, passed=1)


def test_pytest_deprecation_warning(pytester):
    """Assert no deprecation warning is raised during test."""
    p = pytester.makepyfile(
        """
        def hello():
            print("Hello, world!")
    """
    )
    # replace trailing newline (stripped by pytester.makepyfile)
    p = p.write_text(p.read_text() + "\n")

    result = pytester.runpytest("--black")
    result.assert_outcomes(passed=1)

    out = "\n".join(result.stdout.lines)
    assert "PytestUnknownMarkWarning" not in out
