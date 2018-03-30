#!/usr/bin/env python
""" Height Profile Example """
import pyiri2016 as iri
import pyiri2016.plots as piri
#
import numpy as np
from matplotlib.pyplot import  show

glat, glon = -11.95, -76.77

alt_km = np.arange(80,1000,20.)

iono = iri.IRI('2012-08-21T12', alt_km, glat, glon)

piri.altprofile(iono)

show()