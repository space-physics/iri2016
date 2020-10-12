import subprocess
from dateutil.parser import parse
from datetime import datetime
import xarray
import io
import os
import numpy as np
import typing as T
import importlib.resources

iri_name = "iri2016_driver"
if os.name == "nt":
    iri_name += ".exe"

if not importlib.resources.is_resource(__package__, iri_name):
    with importlib.resources.path(__package__, "setup.cmake") as setup:
        subprocess.check_call(["ctest", "-S", str(setup), "-VV"])

SIMOUT = ["ne", "Tn", "Ti", "Te", "nO+", "nH+", "nHe+", "nO2+", "nNO+", "nCI", "nN+"]

__all__ = ["IRI"]


def IRI(time: T.Union[str, datetime], altkmrange: T.Sequence[float], glat: float, glon: float) -> xarray.Dataset:

    if isinstance(time, str):
        time = parse(time)

    assert len(altkmrange) == 3, "altitude (km) min, max, step"
    assert isinstance(glat, (int, float)) and isinstance(glon, (int, float)), "glat, glon is scalar"

    with importlib.resources.path(__package__, iri_name) as exe:
        cmd = [
            str(exe),
            str(time.year),
            str(time.month),
            str(time.day),
            str(time.hour),
            str(time.minute),
            str(time.second),
            str(glat),
            str(glon),
            str(altkmrange[0]),
            str(altkmrange[1]),
            str(altkmrange[2]),
            str(exe.parent / "data"),
        ]

        ret = subprocess.check_output(cmd, text=True)  # str for Windows
    # %% get altitude profile data
    Nalt = int((altkmrange[1] - altkmrange[0]) // altkmrange[2]) + 1

    arr = np.genfromtxt(io.StringIO(ret), max_rows=Nalt)
    arr = np.atleast_2d(arr)
    assert arr.ndim == 2 and arr.shape[1] == 12, "bad text data output format"

    dsf = {k: (("alt_km"), v) for (k, v) in zip(SIMOUT, arr[:, 1:].T)}
    altkm = arr[:, 0]
    # %% get parameter data
    arr = np.genfromtxt(io.StringIO(ret), skip_header=Nalt)
    assert arr.ndim == 1 and arr.size == 100, "bad text data output format"
    # %% assemble output
    iono = xarray.Dataset(
        dsf, coords={"time": [time], "alt_km": altkm, "glat": glat, "glon": glon}, attrs={"f107": arr[40], "ap": arr[51]}
    )

    for i, p in enumerate(["NmF2", "hmF2", "NmF1", "hmF1", "NmE", "hmE"]):
        iono[p] = (("time"), [arr[i]])

    iono["TEC"] = (("time"), [arr[36]])
    iono["EqVertIonDrift"] = (("time"), [arr[43]])
    iono["foF2"] = (("time"), [arr[99]])

    return iono
