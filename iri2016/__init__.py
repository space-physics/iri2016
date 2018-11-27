import subprocess
from dateutil.parser import parse
from datetime import datetime, timedelta
from pathlib import Path
import os
import xarray
import io
import numpy as np
from typing import List, Sequence

R = Path(__file__).resolve().parents[1] / 'bin'
EXE = './iri2016_driver'
SHELL = False
if os.name == 'nt':
    EXE = EXE[2:] + '.exe'
    SHELL = True

SIMOUT = ['ne', 'Tn', 'Ti', 'Te', 'nO+', 'nH+', 'nHe+', 'nO2+', 'nNO+',
          'nCI', 'nN+']


def datetimerange(start: datetime, end: datetime, step: timedelta) -> List[datetime]:
    """like range() for datetime"""
    if isinstance(start, str):
        start = parse(start)

    if isinstance(end, str):
        end = parse(end)

    assert isinstance(start, datetime)
    assert isinstance(end, datetime)
    assert isinstance(step, timedelta)

    return [start + i*step for i in range((end-start) // step)]


def IRI(time: datetime, altkmrange: Sequence[float],
        glat: float, glon: float) -> xarray.Dataset:

    if isinstance(time, str):
        time = parse(time)

    assert len(altkmrange) == 3, 'altitude (km) min, max, step'
    assert isinstance(glat, float) and isinstance(glon, float), 'glat, glon is scalar'

    # NOTE: Windows needs shell=True and str(pathlib.Path)
    cmd = [str(EXE),
           str(time.year), str(time.month), str(time.day),
           str(time.hour), str(time.minute), str(time.second),
           str(glat), str(glon),
           str(altkmrange[0]), str(altkmrange[1]), str(altkmrange[2])]

    ret = subprocess.check_output(cmd,
                                  universal_newlines=True, cwd=str(R),
                                  shell=SHELL)
# %% get altitude profile data
    Nalt = int((altkmrange[1]-altkmrange[0]) // altkmrange[2]) + 1

    arr = np.genfromtxt(io.StringIO(ret), max_rows=Nalt)
    arr = np.atleast_2d(arr)
    assert arr.ndim == 2 and arr.shape[1] == 12, 'bad text data output format'

    dsf = {k: (('alt_km'), v) for (k, v) in zip(SIMOUT, arr[:, 1:].T)}
    altkm = arr[:, 0]
# %% get parameter data
    arr = np.genfromtxt(io.StringIO(ret), skip_header=Nalt)
    assert arr.ndim == 1 and arr.size == 100, 'bad text data output format'
# %% assemble output
    iono = xarray.Dataset(dsf,
                          coords={'time': [time], 'alt_km': altkm,
                                  'glat': glat, 'glon': glon},
                          attrs={'f107': arr[40], 'ap': arr[51]})

    for i, p in enumerate(['NmF2', 'hmF2', 'NmF1', 'hmF1', 'NmE', 'hmE']):
        iono[p] = (('time'), [arr[i]])

    iono['TEC'] = (('time'), [arr[36]])
    iono['EqVertIonDrift'] = (('time'), [arr[43]])

    return iono


def timeprofile(tlim: tuple, dt: timedelta,
                altkmrange: list, glat: float, glon: float) -> xarray.Dataset:
    """compute IRI altitude profile over time range for fixed lat/lon
    """

    T = datetimerange(tlim[0], tlim[1], dt)

    iono: xarray.Dataset = None

    f107 = []
    ap = []
    for t in T:
        iri = IRI(t, altkmrange, glat, glon)
        if iono is None:
            iono = iri
        else:
            iono = xarray.concat((iono, iri), dim='time')

        f107.append(iri.f107)
        ap.append(iri.ap)

    iono.attrs = iri.attrs
    iono.attrs['f107'] = f107
    iono.attrs['ap'] = ap

    return iono


def geoprofile(latrange: Sequence[float], glon: float,
               altkm: float,
               time: datetime) -> xarray.Dataset:
    """compute IRI altitude profiles at time, over lat or lon range
    """

    glat = np.arange(*latrange)

    iono: xarray.Dataset = None

    f107 = []
    ap = []
    for l in glat:
        iri = IRI(time, altkmrange=[altkm]*3, glat=l, glon=glon)
        if iono is None:
            iono = iri
        else:
            iono = xarray.concat((iono, iri), dim='glat')

        f107.append(iri.f107)
        ap.append(iri.ap)

    iono.attrs = iri.attrs
    iono.attrs['f107'] = f107
    iono.attrs['ap'] = ap

    return iono
