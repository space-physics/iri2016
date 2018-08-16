#!/usr/bin/env python
""" Height Profile Example """
import iri2016 as iri
from argparse import ArgumentParser
import numpy as np
from matplotlib.pyplot import show
import iri2016.plots as piri


def main():

    p = ArgumentParser()
    p.add_argument('latlon', help='geodetic latitude, longitude (degrees)',
                   type=float, nargs=2)
    p.add_argument('-alt_km', help='altitude START STOP STEP (km)',
                   type=float, nargs=3, default=(80, 1000, 20))
    p.add_argument('-q', '--quiet', help='disable plotting', action='store_true')
    P = p.parse_args()

    alt_km = np.arange(*P.alt_km)

    iono = iri.IRI('2012-08-21T12', alt_km, *P.latlon)

    if not P.quiet:
        piri.altprofile(iono)
        show()


if __name__ == '__main__':
    main()
