#!/usr/bin/env python
import numpy as np
import unittest
from pyiri2016 import IRI2016

class BasicTests(unittest.TestCase):
    def test_main1(self):

        Obj = IRI2016()
        IRIData, IRIDATAAdd = Obj.IRI(time='1980-03-21T12')
        np.testing.assert_allclose((IRIData['ne'], IRIDATAAdd['NmF2'], IRIDATAAdd['hmF2']),
                        (267285184512.0, 2580958937088.0, 438.78643798828125))

if __name__ == '__main__':
    unittest.main()
