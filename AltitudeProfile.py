#!/usr/bin/env python
""" Height Profile Example """
import pyiri2016 as iri
#
import numpy as np

glat, glon = -11.95, -76.77

alt_km = np.arange(80,1000,20.)

iono = iri.IRI('2012-08-21T12', alt_km, glat, glon)

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('-q','--quiet',help='disable plotting',action='store_true')
    p = p.parse_args()
    
    if not p.quiet:
        from matplotlib.pyplot import  show
        import pyiri2016.plots as piri

        piri.altprofile(iono)
        show()
