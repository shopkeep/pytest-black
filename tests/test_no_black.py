# -*- coding: utf-8 -*-

import pytest


pytestmark = pytest.mark.usefixtures('black_unavailable')


def test_skipped_when_black_unavailable(testdir):
    testdir.makepyfile("")
    result = testdir.runpytest("--black")
    result.assert_outcomes(skipped=1)
