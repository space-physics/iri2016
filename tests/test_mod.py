#!/usr/bin/env python
import numpy as np
import pytest
from pathlib import Path
import iri2016

root = Path(__file__).parents[1]


def test_point():

    iri = iri2016.IRI('1980-03-21T12', 130., 0., 0.)

    np.testing.assert_allclose((iri['ne'].item(), iri.NmF2, iri.hmF2),
                               (267285184512.0, 2580958937088.0, 438.78643798828125))



def test_altitude_profile():
    time = '2015-12-13T10'
    alt_km = np.arange(100,1000,10)
    glat = 65.1
    glon = -147.5

    iri = iri2016.IRI(time, alt_km, glat, glon).squeeze()

    np.testing.assert_allclose(iri['ne'][10], 4.931192e+09)
    np.testing.assert_allclose((iri.NmF2, iri.hmF2),(82.14109e9, 317.35287))


if __name__ == '__main__':
    pytest.main(['-x', __file__])
