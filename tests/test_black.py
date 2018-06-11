# -*- coding: utf-8 -*-


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
