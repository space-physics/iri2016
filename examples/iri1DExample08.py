#!/usr/bin/env python
from pyiri2016 import IRI2016,IRI2016Profile
from numpy import arange
from matplotlib.pyplot import figure, show


def example08():

    """ GMT Profile Example """

    hrlim = [0, 24]
    hrstp = 0.25
    iri2016Obj = IRI2016Profile(hrlim=hrlim, hrstp=hrstp, lat=-11.95,
    lon=-76.77, option=8, verbose=False, time='2004-01-01')

    hrbins = arange(hrlim[0], hrlim[1] + hrstp, hrstp)

    nhr = hrbins.size
    index = range(nhr)

    fig = figure(figsize=(16,12))
    axs = fig.subplots(2,2, sharex=True)

    pn = axs[0,0]
    NmF2 = iri2016Obj.b[0, index]
    NmF1 = IRI2016()._RmNeg(iri2016Obj.b[2, index])
    NmE = iri2016Obj.b[4, index]
    pn.plot(hrbins, NmF2, label='N$_m$F$_2$')
    pn.plot(hrbins, NmF1, label='N$_m$F$_1$')
    pn.plot(hrbins, NmE, label='N$_m$E')
    pn.set_title(iri2016Obj.title1)
    pn.set_xlim(hrbins[[0, -1]])
    pn.set_xlabel('Hour (UT)')
    pn.set_ylabel('(m$^{-3}$)')
    pn.set_yscale('log')
    pn.legend(loc='best')

    pn = axs[0,1]
    hmF2 = iri2016Obj.b[1, index]
    hmF1 = IRI2016()._RmNeg(iri2016Obj.b[3, index])
    hmE = iri2016Obj.b[5, index]
    pn.plot(hrbins, hmF2, label='h$_m$F$_2$')
    pn.plot(hrbins, hmF1, label='h$_m$F$_1$')
    pn.plot(hrbins, hmE, label='h$_m$E')
    pn.set_xlim(hrbins[[0, -1]])
    pn.set_title(iri2016Obj.title2)
    pn.set_xlabel('Hour (UT)')
    pn.set_ylabel('(km)')
    pn.legend(loc='best')

    # pn = axs[1,0]
    # tec = iri2016Obj.b[36, index]
    # pn.plot(hrbins, tec, label=r'TEC')
    # pn.set_xlim(hrbins[[0, -1]])
    # pn.set_xlabel('Hour (UT)')
    # pn.set_ylabel('(m$^{-2}$)')
    # #pn.set_yscale('log')
    # legend(loc='best')

    pn = axs[1,1]
    vy = iri2016Obj.b[43, index]
    pn.plot(hrbins, vy, label=r'V$_y$')
    pn.set_xlim(hrbins[[0, -1]])
    pn.set_xlabel('Hour (UT)')
    pn.set_ylabel('(m/s)')
    pn.legend(loc='best')

    for a in axs.ravel():
        a.grid(True)


if __name__ == '__main__':

    example08()

    show()
