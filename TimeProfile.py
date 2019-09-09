#!/usr/bin/env python
""" Time Profile: IRI2016 """
from datetime import timedelta
from argparse import ArgumentParser
import iri2016 as iri
from matplotlib.pyplot import show
import iri2016.plots as piri


def main():
    p = ArgumentParser()
    p.add_argument("time", help="start yy-mm-dd, stop yy-mm-dd, step_hour", nargs=3)
    p.add_argument("latlon", help="geodetic latitude, longitude (degrees)", nargs=2, type=float)
    p.add_argument("-alt_km", help="altitude START STOP STEP (km)", type=float, nargs=3, default=(100, 200, 20))
    P = p.parse_args()

    sim = iri.timeprofile((P.time[0], P.time[1]), timedelta(hours=float(P.time[2])), P.alt_km, *P.latlon)

    piri.timeprofile(sim)
    show()


if __name__ == "__main__":
    main()
