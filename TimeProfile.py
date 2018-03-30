#!/usr/bin/env python
""" Time Profile: IRI2016 """
import numpy as np
from datetime import timedelta
from matplotlib.pyplot import figure, show
try:
    import ephem
except ImportError:
    ephem = None
#
import pyiri2016


# %% user parameters
#lat = -11.95; lon = -76.77
#glat, glon = 0,0
glat,glon = 65,-148
alt_km = np.arange(120, 180, 20)
# %% ru
sim = pyiri2016.timeprofile(('2012-08-21','2012-08-22'),timedelta(hours=0.25),
                            alt_km,glat,glon)

# %% Plots
Nplot=3

if Nplot>2:
    fig = figure(figsize=(16,12))
    axs = fig.subplots(3,1, sharex=True).ravel()
else:
    fig = figure(figsize=(16,6))
    axs = fig.subplots(1,2).ravel()

fig.suptitle(f'{str(sim.time[0].values)[:-13]} to {str(sim.time[-1].values)[:-13]}\n Glat, Glon: {sim.glat}, {sim.glon}')

ax = axs[0]
#NmF1 = pyiri2016.IRI2016()._RmNeg(sim.b[2, :])
#NmE = sim.loc[4, :]
ax.plot(sim.time, sim['NmF2'].squeeze(), label='N$_m$F$_2$')
#ax.plot(sim.time, NmF1, label='N$_m$F$_1$')
#ax.plot(sim.time, NmE, label='N$_m$E')
ax.set_title('Maximum number densities vs. ionospheric layer')
ax.set_xlabel('Hour (UT)')
ax.set_ylabel('(m$^{-3}$)')
ax.set_yscale('log')
ax.legend(loc='best')

ax = axs[1]
#hmF1 = pyiri2016.IRI2016()._RmNeg(sim.b[3, :])
#hmE = sim.b[5, :]
ax.plot(sim.time, sim['hmF2'].squeeze(), label='h$_m$F$_2$')
#ax.plot(sim.time, hmF1, label='h$_m$F$_1$')
#ax.plot(sim.time, hmE, label='h$_m$E')
ax.set_title('Height of maximum density vs. ionospheric layer')
ax.set_xlabel('Hour (UT)')
ax.set_ylabel('(km)')
ax.legend(loc='best')
# %%
if Nplot > 2:
    ax = axs[2]

    for a in sim.alt_km:
        ax.plot(sim.time, sim['ne'].squeeze(), marker='.', label=f'{a.item()} km')
    ax.set_xlabel('time UTC (hours)')
    ax.set_ylabel('[m$^{-3}$]')
    ax.set_title(f'$N_e$ vs. altitude and time')
    ax.set_yscale('log')
    ax.legend(loc='best')
# %%
if Nplot > 4:
    ax = axs[4]
    tec = sim.b[36, :]
    ax.plot(sim.time, tec, label=r'TEC')
    ax.set_xlabel('Hour (UT)')
    ax.set_ylabel('(m$^{-2}$)')
    #ax.set_yscale('log')
    ax.legend(loc='best')

    ax = axs[5]
    vy = sim.b[43, :]
    ax.plot(sim.time, vy, label=r'V$_y$')
    ax.set_xlabel('Hour (UT)')
    ax.set_ylabel('(m/s)')
    ax.legend(loc='best')

for a in axs.ravel():
    a.grid(True)


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='IRI2016 time profile plot')
    p.add_argument('-t','--trange',help='START STOP STEP (hours) time [UTC]',nargs=3,
                   default=('2012-08-21','2012-08-22',0.25))
    p.add_argument('--alt',help='START STOP STEP altitude [km]',type=float, nargs=3,default=(120,180,20))
    p.add_argument('-c','--latlon',help='geodetic coordinates of simulation',
                   type=float,default=(65,-147.5))
    p.add_argument('--f107',type=float,default=200.)
    p.add_argument('--f107a', type=float,default=200.)
    p.add_argument('--ap', type=int, default=4)
    p.add_argument('--species',help='species to plot',nargs='+',default=('ne'))
    p = p.parse_args()


show()
