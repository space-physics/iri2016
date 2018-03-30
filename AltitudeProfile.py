#!/usr/bin/env python
""" Height Profile Example """
import pyiri2016
#
import numpy as np
from matplotlib.pyplot import figure, show

glat, glon = -11.95, -76.77

alt_km = np.arange(80,1000,20.)

iri = pyiri2016.IRI('2012-08-21T12', alt_km, glat, glon)

fig = figure(figsize=(16,6))
axs = fig.subplots(1,2)

fig.suptitle(f'{str(iri.time[0].values)[:-13]}\n Glat, Glon: {iri.glat}, {iri.attrs["glon"]}')


pn = axs[0]
pn.plot(iri['ne'].squeeze(), iri.alt_km, label='N$_e$')
#pn.set_title(iri2016Obj.title1)
pn.set_xlabel('Density (m$^{-3}$)')
pn.set_ylabel('Altitude (km)')
pn.set_xscale('log')
pn.legend(loc='best')
pn.grid(True)

pn = axs[1]
pn.plot(iri['Ti'].squeeze(), iri.alt_km, label='T$_i$')
pn.plot(iri['Te'].squeeze(), iri.alt_km, label='T$_e$')
#pn.set_title(iri2016Obj.title2)
pn.set_xlabel('Temperature (K)')
pn.set_ylabel('Altitude (km)')
pn.legend(loc='best')
pn.grid(True)

show()