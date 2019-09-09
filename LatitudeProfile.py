#!/usr/bin/env python
import iri2016 as iri
from argparse import ArgumentParser
from matplotlib.pyplot import show
from pathlib import Path
import iri2016.plots as piri


def main():
    p = ArgumentParser()
    p.add_argument("glon", help="geodetic  longitude (degrees)", type=float)
    p.add_argument("-glat", help="geodetic latitude START STOP STEP (degrees)", type=float, nargs=3, default=(-60, 60, 2.0))
    p.add_argument("-alt_km", help="altitude (km)", type=float, default=300.0)
    p.add_argument("-o", "--outfn", help="write data to file")
    P = p.parse_args()

    iono = iri.geoprofile(latrange=P.glat, glon=P.glon, altkm=P.alt_km, time="2004-01-01T17")

    if P.outfn:
        outfn = Path(P.outfn).expanduser()
        print("writing", outfn)
        iono.to_netcdf(outfn)

    piri.latprofile(iono)
    show()


if __name__ == "__main__":
    main()
