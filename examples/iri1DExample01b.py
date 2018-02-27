#!/usr/bin/env python
from pyiri2016 import IRI2016Profile
from numpy import arange
from matplotlib.pyplot import figure, legend, show


def example01(lat,lon,time):

    """ Height Profile Example """

    altlim = [90., 200.]
    altstp = 2.

    iri2016Obj = IRI2016Profile(altlim=altlim, altstp=altstp, lat=lat,
        lon=lon, time=time, option=1, verbose=False)

    altbins = arange(altlim[0], altlim[1] + altstp, altstp)

    index = range(altbins.size)

    fig = figure(figsize=(16,6))
    axs = fig.subplots(1,2)

    ne = iri2016Obj.a[0, index]

    nO2p = iri2016Obj.a[7, index] * ne * 1e-2
    nNOp = iri2016Obj.a[8, index] * ne * 1e-2
    #nOp = iri2016Obj.a[5, index] * ne * 1e-2

    pn = axs[0]
    pn.plot(ne, altbins, label='N$_e$')
    pn.plot(nO2p, altbins, label='O$_2$$^+$')
    pn.plot(nNOp, altbins, label='NO$^+$')
    #pn.plot(nOp, altbins, label='O$^+$')
    pn.set_title(iri2016Obj.title1)
    pn.set_xlabel('Density (m$^{-3}$)')
    pn.set_ylabel('Altitude (km)')
    pn.set_xscale('log')
    legend(loc='best')

    pn = axs[1]
    ti = iri2016Obj.a[2, index]
    te = iri2016Obj.a[3, index]
    pn.plot(ti, altbins, label='T$_i$')
    pn.plot(te, altbins, label='T$_e$')
    pn.set_title(iri2016Obj.title2)
    pn.set_xlabel('Temperature ($^\circ$K)')
    pn.set_ylabel('Altitude (km)')
    legend(loc='best')


if __name__ == '__main__':

    example01(lat=-11.95, lon=-76.77,
              time='2003-11-21')

    show()
