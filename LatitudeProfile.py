#!/usr/bin/env python
import pyiri2016
from numpy import arange
from matplotlib.pyplot import figure,  show

""" Geog. Latitude Profile Example """

latlim = [-60, 60]
latstp = 2.
sim = pyiri2016.geoprofile(altkm=600, latlim=latlim, dlat=latstp, \
glon=-76.77,   time='2004-01-01T17')

latbins = arange(latlim[0], latlim[1], latstp)


fig = figure(figsize=(8,12))
axs = fig.subplots(2,1, sharex=True)

pn = axs[0]

pn.plot(latbins, sim['NmF2'].squeeze(), label='N$_m$F$_2$')
pn.plot(latbins, sim['NmF1'].squeeze(), label='N$_m$F$_1$')
pn.plot(latbins, sim['NmE'].squeeze(), label='N$_m$E')
pn.set_title(str(sim.time[0].values)[:-13] + '  latitude'+str(latlim))
pn.set_xlim(latbins[[0, -1]])
pn.set_xlabel('Geog. Lat. ($^\circ$)')
pn.set_ylabel('(m$^{-3}$)')
pn.set_yscale('log')


pn = axs[1]
pn.plot(latbins, sim['hmF2'].squeeze(), label='h$_m$F$_2$')
pn.plot(latbins, sim['hmF1'].squeeze(), label='h$_m$F$_1$')
pn.plot(latbins, sim['hmE'].squeeze(), label='h$_m$E')
pn.set_xlim(latbins[[0, -1]])
pn.set_title(str(sim.time[0].values)[:-13] + '  latitude'+str(latlim))
pn.set_xlabel('Geog. Lat. ($^\circ$)')
pn.set_ylabel('(km)')

for a in axs:
    a.legend(loc='best')
    a.grid(True)


show()
