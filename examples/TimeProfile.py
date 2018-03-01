#!/usr/bin/env python
from pyiri2016 import IRI2016,IRI2016Profile
from numpy import arange
from matplotlib.pyplot import figure, show

""" Time Profile Example """

hrlim = [0, 24] # [0,24] does whole day(s)
hrstp = 0.1 # time step [decimal hours]
#lat = -11.95; lon = -76.77
lat = 65; lon = -147.5
alts = arange(100, 200, 10)
sim = IRI2016Profile(hrlim=hrlim, hrstp=hrstp, lat=lat, lon=lon, alt=150.,
                     option='time', verbose=False, time='2017-08-21')

hrbins = arange(hrlim[0], hrlim[1] + hrstp, hrstp)

nhr = hrbins.size
index = range(nhr)

Nplot=4


if Nplot>2:
    fig = figure(1,figsize=(16,12))
    axs = fig.subplots(2,2, sharex=True).ravel()
else:
    fig = figure(1,figsize=(16,6))
    axs = fig.subplots(1,2).ravel()

pn = axs[0]
NmF2 = sim.b[0, index]
NmF1 = IRI2016()._RmNeg(sim.b[2, index])
NmE = sim.b[4, index]
pn.plot(hrbins, NmF2, label='N$_m$F$_2$')
pn.plot(hrbins, NmF1, label='N$_m$F$_1$')
pn.plot(hrbins, NmE, label='N$_m$E')
pn.set_title(sim.title1)
pn.set_xlim(hrbins[[0, -1]])
pn.set_xlabel('Hour (UT)')
pn.set_ylabel('(m$^{-3}$)')
pn.set_yscale('log')
pn.legend(loc='best')

pn = axs[1]
hmF2 = sim.b[1, index]
hmF1 = IRI2016()._RmNeg(sim.b[3, index])
hmE = sim.b[5, index]
pn.plot(hrbins, hmF2, label='h$_m$F$_2$')
pn.plot(hrbins, hmF1, label='h$_m$F$_1$')
pn.plot(hrbins, hmE, label='h$_m$E')
pn.set_xlim(hrbins[[0, -1]])
pn.set_title(sim.title2)
pn.set_xlabel('Hour (UT)')
pn.set_ylabel('(km)')
pn.legend(loc='best')

if Nplot > 2:
    pn = axs[2]

    for alt in alts:
        sim = IRI2016Profile(hrlim=hrlim, hrstp=hrstp, lat=lat, lon=lon, alt=alt,
                             option='time', verbose=False, time='2017-08-10')

        pn.plot(sim.out.time, sim.out.loc[:,'ne'], marker='.', label=alt)
    pn.set_xlabel('time UTC (hours)')
    pn.set_ylabel('[m$^{-3}$]')
    pn.set_title(f'$N_e$ vs. altitude and time')
    pn.legend(loc='best')

if Nplot > 4:
    pn = axs[4]
    tec = sim.b[36, index]
    pn.plot(hrbins, tec, label=r'TEC')
    pn.set_xlim(hrbins[[0, -1]])
    pn.set_xlabel('Hour (UT)')
    pn.set_ylabel('(m$^{-2}$)')
    #pn.set_yscale('log')
    pn.legend(loc='best')

    pn = axs[5]
    vy = sim.b[43, index]
    pn.plot(hrbins, vy, label=r'V$_y$')
    pn.set_xlim(hrbins[[0, -1]])
    pn.set_xlabel('Hour (UT)')
    pn.set_ylabel('(m/s)')
    pn.legend(loc='best')

for a in axs.ravel():
    a.grid(True)



show()
