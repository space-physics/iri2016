#!/usr/bin/env python
from iri2016.iri2016prof2D import IRI2016_2DProf


iri2016Obj = IRI2016_2DProf(
    altlim=[100.0, 1000.0],
    altstp=5.0,
    hrstp=0.25 / 3,
    lat=-11.95,
    lon=-76.77,
    time="2017-06-01",
    option=1,
)
iri2016Obj.HeightVsTime()
iri2016Obj.Plot2D()
