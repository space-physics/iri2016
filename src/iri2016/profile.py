import xarray
from dateutil.parser import parse
from datetime import datetime, timedelta
import typing as T
import numpy as np

from .base import IRI

__all__ = ["datetimerange", "timeprofile", "geoprofile"]


def datetimerange(start: datetime, end: datetime, step: timedelta) -> T.List[datetime]:
    """like range() for datetime"""
    if isinstance(start, str):
        start = parse(start)

    if isinstance(end, str):
        end = parse(end)

    assert isinstance(start, datetime)
    assert isinstance(end, datetime)
    assert isinstance(step, timedelta)

    return [start + i * step for i in range((end - start) // step)]


def timeprofile(tlim: tuple, dt: timedelta, altkmrange: T.Sequence[float], glat: float, glon: float) -> xarray.Dataset:
    """compute IRI altitude profile over time range for fixed lat/lon"""

    times = datetimerange(tlim[0], tlim[1], dt)

    iono: xarray.Dataset = None

    f107 = []
    ap = []
    for time in times:
        iri = IRI(time, altkmrange, glat, glon)
        if iono is None:
            iono = iri
        else:
            iono = xarray.concat((iono, iri), dim="time")

        f107.append(iri.f107)
        ap.append(iri.ap)

    iono.attrs = iri.attrs
    iono.attrs["f107"] = f107
    iono.attrs["ap"] = ap

    return iono


def geoprofile(latrange: T.Union[float, T.Sequence[float]], lonrange: T.Union[float, T.Sequence[float]], altkm: float, time: T.Union[str, datetime]) -> xarray.Dataset:
    """compute IRI altitude profiles at time, over lat or lon range"""
    
    if isinstance(latrange, (T.Sequence, np.ndarray)):
        glat = np.arange(*latrange, dtype=np.float)
    else:
        glat = np.atleast_1d(np.float(latrange))
        
    if isinstance(lonrange, (T.Sequence, np.ndarray)):
        glon = np.arange(*lonrange, dtype=np.float)
    else:
        glon = np.atleast_1d(np.float(lonrange))
    
    iono: xarray.Dataset = None

    f107 = []
    ap = []
    for lt in glat:
        iono_lons: xarray.Dataset = None

        for ln in glon:
            iri = IRI(time, altkmrange=[altkm] * 3, glat=lt, glon=ln)
            if iono_lons is None:
                iono_lons = iri
            else:
                iono_lons = xarray.concat((iono_lons, iri), dim="glon")

        if iono is None:
            iono = iono_lons
        else:
            iono = xarray.concat((iono, iono_lons), dim="glat")

        f107.append(iri.f107)
        ap.append(iri.ap)

    iono.attrs = iri.attrs
    iono.attrs["f107"] = f107
    iono.attrs["ap"] = ap

    return iono
