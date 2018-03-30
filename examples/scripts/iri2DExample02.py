#!/usr/bin/env python
    # 2D Example: Lat vs Lon, Earth's Map
from pyiri2016.iri2016prof2D import IRI2016_2DProf


lonstp = 4

iri2016Obj = IRI2016_2DProf(lat=-11.95, latstp=2., lon=-76.77, lonstp=lonstp,
                            time = '2010-09-01T17',
                            option=2)
iri2016Obj.LatVsLon(lonstp=lonstp)
iri2016Obj.Plot2D()
