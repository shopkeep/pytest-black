import importlib

import pytest


pytest_plugins = "pytester"


@pytest.fixture
def black_available():
    pytest.importorskip('black')


@pytest.fixture
def black_unavailable():
    try:
        importlib.import_module('black')
        pytest.skip("Black is available")
    except ImportError:
        return
