#!/usr/bin/env python
from pyiri2016 import IRI2016


if __name__ == '__main__':

    def main1():

        Obj = IRI2016()
        IRIData, IRIDATAAdd = Obj.IRI()
        print(IRIData['ne'])
        print(IRIDATAAdd['NmF2'], IRIDATAAdd['hmF2'])


    main1()
