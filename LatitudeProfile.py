#!/usr/bin/env python
import pyiri2016 as iri
import pyiri2016.plots as piri
from matplotlib.pyplot import show

""" Geog. Latitude Profile Example """


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('-o','--outfn',help='write data to file')
    p = p.parse_args()

    latlim = [-60, 60]
    latstp = 2.
    iono = iri.geoprofile(altkm=600, latlim=latlim, dlat=latstp,
                          glon=-76.77,   time='2004-01-01T17')

    piri.latprofile(iono)


    show()
