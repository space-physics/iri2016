#!/usr/bin/env python
""" Time Profile: IRI2016 """
import numpy as np
from datetime import timedelta
from matplotlib.pyplot import show
#
import pyiri2016 as iri
import pyiri2016.plots as piri


# %% user parameters
#lat = -11.95; lon = -76.77
#glat, glon = 0,0
glat,glon = 65,-148
alt_km = np.arange(120, 180, 20)
# %% ru
sim = iri.timeprofile(('2012-08-21','2012-08-22'),timedelta(hours=0.25),
                            alt_km,glat,glon)

piri.timeprofile(sim)

show()
