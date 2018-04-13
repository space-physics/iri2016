#!/usr/bin/env python
import pyiri2016 as iri
import pyiri2016.plots as piri
from matplotlib.pyplot import show
""" Geog. Latitude Profile Example """



latlim = [-60, 60]
latstp = 2.
iono = iri.geoprofile(altkm=600, latlim=latlim, dlat=latstp, glon=-76.77, time='2004-01-01T17')



if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('-o','--outfn',help='write data to file')
    p.add_argument('-q','--quiet',help='disable plotting',action='store_true')
    p = p.parse_args()
    
    
    
    if not p.quiet:
      from matplotlib.pyplot import show
      import pyiri2016.plots as piri

      piri.latprofile(iono)
      show()
