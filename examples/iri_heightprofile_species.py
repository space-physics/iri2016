#!/usr/bin/env python
from iri2016 import IRI2016Profile
#
import numpy as np
from matplotlib.pyplot import figure,  show
""" Height Profile Example """

lat = -11.95
lon = -76.77
time = '2003-11-21T12'
altlim = [90., 200.]
altstp = 2.

sim = IRI2016Profile(altlim=altlim, altstp=altstp, lat=lat,
                     lon=lon, time=time, option='vertical', verbose=False)

altbins = np.arange(altlim[0], altlim[1] + altstp, altstp)

index = range(altbins.size)

fig = figure(figsize=(16, 6))
axs = fig.subplots(1, 2)

ne = sim.a[0, index]

nO2p = sim.a[7, index] * ne * 1e-2
nNOp = sim.a[8, index] * ne * 1e-2
# nOp = sim.a[5, index] * ne * 1e-2

pn = axs[0]
pn.plot(ne, altbins, label='N$_e$')
pn.plot(nO2p, altbins, label='O$_2$$^+$')
pn.plot(nNOp, altbins, label='NO$^+$')
# pn.plot(nOp, altbins, label='O$^+$')
pn.set_title(sim.title1)
pn.set_xlabel('Density (m$^{-3}$)')
pn.set_ylabel('Altitude (km)')
pn.set_xscale('log')

pn = axs[1]
ti = sim.a[2, index]
te = sim.a[3, index]
pn.plot(ti, altbins, label='T$_i$')
pn.plot(te, altbins, label='T$_e$')
pn.set_title(sim.title2)
pn.set_xlabel('Temperature ($^\circ$K)')
pn.set_ylabel('Altitude (km)')


for a in axs:
    a.legend(loc='best')
    a.grid(True)

show()
