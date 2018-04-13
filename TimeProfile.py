#!/usr/bin/env python
""" Time Profile: IRI2016 """
import numpy as np
from datetime import timedelta
#
import pyiri2016 as iri

# %% user parameters
#lat = -11.95; lon = -76.77
#glat, glon = 0,0
glat,glon = 65,-148
alt_km = np.arange(120, 180, 20)
# %% ru
sim = iri.timeprofile(('2012-08-21','2012-08-22'),timedelta(hours=0.25),
                            alt_km,glat,glon)

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('-q','--quiet',help='disable plotting',action='store_true')
    p = p.parse_args()


    if not p.quiet:
        from matplotlib.pyplot import show
        import pyiri2016.plots as piri
        
        piri.timeprofile(sim)
        show()
