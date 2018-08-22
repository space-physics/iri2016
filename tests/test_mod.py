#!/usr/bin/env python
from pytest import approx
import pytest
import numpy as np
from pathlib import Path
import iri2016

root = Path(__file__).parents[1]


def test_point():

    iri = iri2016.IRI('1980-03-21T12', 130., 0., 0.)

    assert [iri['ne'].item(), iri.NmF2, iri.hmF2] == approx([267285184512.0, 2580958937088.0, 438.78643798828125],
                                                            rel=1e-4)


def test_altitude_profile():
    time = '2015-12-13T10'
    alt_km = np.arange(100, 1000, 10)
    glat = 65.1
    glon = -147.5

    iri = iri2016.IRI(time, alt_km, glat, glon).squeeze()

    assert iri['ne'][10] == approx(4.931192e+09, rel=1e-4)
    assert (iri.NmF2, iri.hmF2) == approx((82.14109e9, 317.35287), rel=1e-4)


if __name__ == '__main__':
    pytest.main(['-xv', __file__])
