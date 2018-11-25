import subprocess
from dateutil.parser import parse
from pathlib import Path
import os
import xarray
import io
import numpy as np

R = Path(__file__).resolve().parents[1] / 'bin'
EXE = './iri2016_driver'
if os.name == 'nt':
    EXE = EXE[2:] + '.exe'

SIMOUT = ['ne', 'Tn', 'Ti', 'Te', 'nO+', 'nH+', 'nHe+', 'nO2+', 'nNO+',
          'nCI', 'nN+']


def IRI(time, altkmrange, glat: float, glon: float) -> xarray.Dataset:

    if isinstance(time, str):
        time = parse(time)

    assert len(altkmrange) == 3, 'altitude (km) min, max, step'
    assert isinstance(glat, float) and isinstance(glon, float), 'for now, glat, glon is scalar'

    ret = subprocess.check_output([str(EXE),
                                   str(time.year), str(time.month), str(time.day),
                                   str(time.hour), str(time.minute), str(time.second),
                                   str(glat), str(glon),
                                   str(altkmrange[0]), str(altkmrange[1]), str(altkmrange[2])],
                                  universal_newlines=True, cwd=R)

    arr = np.loadtxt(io.StringIO(ret))

    dsf = {k: (('alt_km'), v) for (k, v) in zip(SIMOUT, arr[:, 1:].T)}

    iono = xarray.Dataset(dsf,
                          coords={'alt_km': arr[:, 0]},
                          attrs={'time': time, 'glat': glat, 'glon': glon})

    return iono
