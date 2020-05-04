# -*- coding: utf-8 -*-

# stdlib imports
import subprocess
import re
import sys

# third-party imports
import pytest
import toml


HISTKEY = "black/mtimes"


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption(
        "--black", action="store_true", help="enable format checking with black"
    )


def pytest_collect_file(path, parent):
    config = parent.config
    if config.option.black and path.ext == ".py":
        if hasattr(BlackItem, "from_parent"):
            return BlackItem.from_parent(parent, fspath=path)
        else:
            return BlackItem(path, parent)


def pytest_configure(config):
    # load cached mtimes at session startup
    if config.option.black and hasattr(config, "cache"):
        config._blackmtimes = config.cache.get(HISTKEY, {})
    config.addinivalue_line("markers", "black: enable format checking with black")


def pytest_unconfigure(config):
    # save cached mtimes at end of session
    if hasattr(config, "_blackmtimes"):
        config.cache.set(HISTKEY, config._blackmtimes)


class BlackItem(pytest.Item, pytest.File):
    def __init__(self, fspath, parent):
        super(BlackItem, self).__init__(fspath, parent)
        self._nodeid += "::BLACK"
        self.add_marker("black")
        try:
            with open("pyproject.toml") as toml_file:
                self.pyproject = toml.load(toml_file)["tool"]["black"]
        except Exception:
            self.pyproject = {}

    def setup(self):
        pytest.importorskip("black")
        mtimes = getattr(self.config, "_blackmtimes", {})
        self._blackmtime = self.fspath.mtime()
        old = mtimes.get(str(self.fspath), 0)
        if self._blackmtime == old:
            pytest.skip("file(s) previously passed black format checks")

        if self._skip_test():
            pytest.skip("file(s) excluded by pyproject.toml")

    def runtest(self):
        cmd = [sys.executable, "-m", "black", "--check", "--diff", "--quiet", str(self.fspath)]
        try:
            subprocess.run(
                cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True
            )
        except subprocess.CalledProcessError as e:
            raise BlackError(e)

        mtimes = getattr(self.config, "_blackmtimes", {})
        mtimes[str(self.fspath)] = self._blackmtime

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(BlackError):
            return excinfo.value.args[0].stdout
        return super(BlackItem, self).repr_failure(excinfo)

    def reportinfo(self):
        return (self.fspath, -1, "Black format check")

    def _skip_test(self):
        return self._excluded() or (not self._included())

    def _included(self):
        if "include" not in self.pyproject:
            return True
        return re.search(self.pyproject["include"], str(self.fspath))

    def _excluded(self):
        if "exclude" not in self.pyproject:
            return False
        return re.search(self.pyproject["exclude"], str(self.fspath))


class BlackError(Exception):
    pass
