#!/usr/bin/env python
from pyiri2016 import IRI2016Profile
from numpy import arange
from matplotlib.pyplot import figure, show


def example01():

    """ Height Profile Example """

    altlim = [100., 1000.]
    altstp = 5.
    lat, lon = -11.95, -76.77

    iri2016Obj = IRI2016Profile(altlim=altlim, altstp=altstp, lat=lat, \
        lon=lon, time='2003-11-21', option=1, verbose=False)

    altbins = arange(altlim[0], altlim[1] + altstp, altstp)

    index = range(altbins.size)

    fig = figure(figsize=(16,6))
    axs = fig.subplots(1,2)

    pn = axs[0]
    ne = iri2016Obj.a[0, index]
    pn.plot(ne, altbins, label='N$_e$')
    pn.set_title(iri2016Obj.title1)
    pn.set_xlabel('Density (m$^{-3}$)')
    pn.set_ylabel('Altitude (km)')
    pn.set_xscale('log')
    pn.legend(loc='best')
    pn.grid(True)

    pn = axs[1]
    ti = iri2016Obj.a[2, index]
    te = iri2016Obj.a[3, index]
    pn.plot(ti, altbins, label='T$_i$')
    pn.plot(te, altbins, label='T$_e$')
    pn.set_title(iri2016Obj.title2)
    pn.set_xlabel('Temperature (K)')
    pn.set_ylabel('Altitude (km)')
    pn.legend(loc='best')
    pn.grid(True)


if __name__ == '__main__':

    example01()


    show()

