#!/usr/bin/env python
import numpy as np
import pytest
from pathlib import Path
import iri2016

root = Path(__file__).parents[1]


def test_main():

    iri = iri2016.IRI('1980-03-21T12', 130., 0., 0.)

    np.testing.assert_allclose((iri['ne'].item(), iri.NmF2, iri.hmF2),
                               (267285184512.0, 2580958937088.0, 438.78643798828125))

    print('assert passed')


if __name__ == '__main__':
    pytest.main(['-x', __file__])
