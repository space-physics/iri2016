#!/usr/bin/env python
import pyiri2016 as iri
from argparse import ArgumentParser
try:
    from matplotlib.pyplot import show
    import pyiri2016.plots as piri
except ImportError as e:
    print(e)
    piri = None  # type: ignore


def main():
    p = ArgumentParser()
    p.add_argument('glon', help='geodetic  longitude (degrees)',
                   type=float)
    p.add_argument('-glat', help='geodetic latitude START STOP STEP (degrees)',
                   type=float, nargs=3, default=(-60, 60, 2))
    p.add_argument('-alt_km', help='altitude (km)',
                   type=float, default=300)
    p.add_argument('-o', '--outfn', help='write data to file')
    p.add_argument('-q', '--quiet', help='disable plotting', action='store_true')
    P = p.parse_args()

    iono = iri.geoprofile(altkm=P.alt_km,
                          latlim=(P.glat[0], P.glat[1]),
                          dlat=P.glat[2],
                          glon=P.glon,
                          time='2004-01-01T17')

    if not P.quiet and piri is not None:
        piri.latprofile(iono)
        show()


if __name__ == '__main__':
    main()
