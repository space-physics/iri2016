#!/usr/bin/env python
""" Time Profile: IRI2016 """
import numpy as np
from datetime import timedelta
from argparse import ArgumentParser
import iri2016 as iri
try:
    from matplotlib.pyplot import show
    import iri2016.plots as piri
except ImportError as e:
    print(e)
    piri = None  # type: ignore


def main():
    p = ArgumentParser()
    p.add_argument('latlon', help='geodetic latitude, longitude (degrees)',
                   type=float, nargs=2)
    p.add_argument('-alt_km', help='altitude START STOP STEP (km)',
                   type=float, nargs=3, default=(120, 180, 20))
    p.add_argument('-q', '--quiet', help='disable plotting', action='store_true')
    P = p.parse_args()

    alt_km = np.arange(*P.alt_km)

    sim = iri.timeprofile(('2012-08-21', '2012-08-22'), timedelta(hours=0.25),
                          alt_km, *P.latlon)

    if not P.quiet and piri is not None:
        piri.timeprofile(sim)
        show()


if __name__ == '__main__':
    main()
