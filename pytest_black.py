# -*- coding: utf-8 -*-

# stdlib imports
import subprocess

# third-party imports
import pytest

HISTKEY = "black/mtimes"


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption(
        "--black", action="store_true", help="enable format checking with black"
    )


def pytest_collect_file(path, parent):
    config = parent.config
    if config.option.black and path.ext == ".py":
        return BlackItem(path, parent)


def pytest_configure(config):
    # load cached mtimes at session startup
    if config.option.black and hasattr(config, "cache"):
        config._blackmtimes = config.cache.get(HISTKEY, {})


def pytest_unconfigure(config):
    # save cached mtimes at end of session
    if hasattr(config, "_blackmtimes"):
        config.cache.set(HISTKEY, config._blackmtimes)


class BlackItem(pytest.Item, pytest.File):
    def __init__(self, path, parent):
        super(BlackItem, self).__init__(path, parent)
        self._nodeid += "::BLACK"
        self.add_marker("black")

    def setup(self):
        mtimes = getattr(self.config, "_blackmtimes", {})
        self._blackmtime = self.fspath.mtime()
        old = mtimes.get(str(self.fspath), 0)
        if self._blackmtime == old:
            pytest.skip("file(s) previously passed black format checks")

    def runtest(self):
        cmd = ["black", "--check", "--diff", "--quiet", str(self.fspath)]
        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                universal_newlines=True,
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


class BlackError(Exception):
    pass
