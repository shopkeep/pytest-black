# -*- coding: utf-8 -*-

# stdlib imports
import subprocess

# third-party imports
import pytest


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption(
        "--black", action="store_true", help="enable format checking with black"
    )


def pytest_collect_file(path, parent):
    config = parent.config
    if config.option.black and path.ext == ".py":
        return BlackItem(path, parent)


class BlackItem(pytest.Item, pytest.File):
    def __init__(self, path, parent):
        super(BlackItem, self).__init__(path, parent)
        self._nodeid += "::BLACK"
        self.add_marker("black")

    def runtest(self):
        cmd = "black --check --diff --quiet {}".format(self.fspath)
        try:
            subprocess.run(
                cmd,
                check=True,
                shell=True,
                stdout=subprocess.PIPE,
                universal_newlines=True,
            )
        except subprocess.CalledProcessError as e:
            raise BlackError(e)

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(BlackError):
            return excinfo.value.args[0].stdout
        return super(BlackItem, self).repr_failure(excinfo)

    def reportinfo(self):
        return (self.fspath, -1, "Black format check")


class BlackError(Exception):
    pass
