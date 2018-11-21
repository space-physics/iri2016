#!/usr/bin/env python
from pytest import approx
import pytest
from pathlib import Path
import iri2016

root = Path(__file__).parents[1]


def test_altitude_profile():
    time = '2015-12-13T10'
    altkmrange = (100, 1000, 10.)
    glat = 65.1
    glon = -147.5

    iri = iri2016.IRI(time, altkmrange, glat, glon).squeeze()

    assert iri['ne'][10] == approx(3.986688e+09, rel=1e-4)
    assert iri.NmF2 == approx(7.716244e+10)
    assert iri.hmF2 == approx(312.8377)


if __name__ == '__main__':
    pytest.main(['-xv', __file__])
