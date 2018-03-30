#!/usr/bin/env python
from pyiri2016 import IRI


IRIData, IRIDATAAdd = IRI()
print('Ne {:.3e}'.format(IRIData['ne']))
print('NmF2 {:.3e}'.format(IRIDATAAdd['NmF2']))
print('hmF2 {:.3e}'.format(IRIDATAAdd['hmF2']))
