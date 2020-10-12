from .profile import geoprofile

from pathlib import Path
from argparse import ArgumentParser
import typing as T


def main(time: str, alt_km: float, glat: T.Sequence[float], glon: float, outfn: Path = None):
    """ latitude Profile Example """

    iono = geoprofile(latrange=glat, glon=glon, altkm=alt_km, time=time)

    if outfn:
        outfn = Path(outfn).expanduser()
        print("writing", outfn)
        iono.to_netcdf(outfn)

    return iono


def cli():
    p = ArgumentParser(description="IRI2016 latitude profile")
    p.add_argument("time", help="time of simulation")
    p.add_argument("glon", help="geodetic  longitude (degrees)", type=float)
    p.add_argument("-glat", help="geodetic latitude START STOP STEP (degrees)", type=float, nargs=3, default=(-60, 60, 2.0))
    p.add_argument("-alt_km", help="altitude (km)", type=float, default=300.0)
    p.add_argument("-o", "--outfn", help="write data to file")
    P = p.parse_args()

    iono = main(P.time, P.alt_km, P.glat, P.glon, P.outfn)

    try:
        from matplotlib.pyplot import show
        import iri2016.plots as piri

        piri.latprofile(iono)
        show()
    except ImportError:
        pass


if __name__ == "__main__":
    cli()
