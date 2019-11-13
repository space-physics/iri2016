#!/usr/bin/env python
from pytest import approx
import pytest
from pathlib import Path
import iri2016

root = Path(__file__).parents[1]


def test_altitude_profile():
    time = "2015-12-13T10"
    altkmrange = (100, 1000, 10.0)
    glat = 65.1
    glon = -147.5

    iri = iri2016.IRI(time, altkmrange, glat, glon)

    # .item() necessary for stability across OS, pytest versions, etc.
    assert iri["ne"][10].item() == approx(3.98669824e9, rel=1e-4)
    assert iri.NmF2.item() == approx(7.71626844e10, rel=1e-4)
    assert iri.hmF2.item() == approx(312.837677, rel=1e-4)


if __name__ == "__main__":
    pytest.main([__file__])
