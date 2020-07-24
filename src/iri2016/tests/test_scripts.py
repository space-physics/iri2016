import pytest

import subprocess
import os


@pytest.mark.skipif(os.environ.get("CI") is not None, reason="CI no display")
def test_latitude():
    pytest.importorskip("matplotlib")
    subprocess.check_call(["iri2016_latitude", "-148"])


@pytest.mark.skipif(os.environ.get("CI") is not None, reason="CI no display")
def test_time():
    pytest.importorskip("matplotlib")
    subprocess.check_call(["iri2016_time", "2012-01-01", "2012-01-02", "1.0", "65", "-148"])


@pytest.mark.skipif(os.environ.get("CI") is not None, reason="CI no display")
def test_alt():
    pytest.importorskip("matplotlib")
    subprocess.check_call(["iri2016_altitude", "2012-01-01", "65", "-148"])
