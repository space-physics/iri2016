#!/usr/bin/env python
""" Height Profile Example """
import iri2016 as iri
from argparse import ArgumentParser
from matplotlib.pyplot import show
import iri2016.plots as piri


def main():

    p = ArgumentParser()
    p.add_argument('latlon', help='geodetic latitude, longitude (degrees)',
                   type=float, nargs=2)
    p.add_argument('-alt_km', help='altitude START STOP STEP (km)',
                   type=float, nargs=3, default=(80, 1000, 10))
    P = p.parse_args()

    iono = iri.IRI('2012-08-21T12', P.alt_km, *P.latlon)

    piri.altprofile(iono)
    show()


if __name__ == '__main__':
    main()
