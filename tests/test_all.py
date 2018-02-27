#!/usr/bin/env python
from numpy.testing import run_module_suite,assert_allclose
from pyiri2016 import IRI2016

def test_main1():

    Obj = IRI2016()
    IRIData, IRIDATAAdd = Obj.IRI(time='1980-03-21T12')
    assert_allclose((IRIData['ne'], IRIDATAAdd['NmF2'], IRIDATAAdd['hmF2']),
                    (267285184512.0, 2580958937088.0, 438.78643798828125))

if __name__ == '__main__':
    run_module_suite()
