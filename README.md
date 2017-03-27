[![alt tag](https://zenodo.org/badge/DOI/10.5281/zenodo.240895.svg)](https://doi.org/10.5281/zenodo.240895)

# pyIRI2016

![alt tag](figures/iri2DExample02.gif)

A Python interface to the International Reference Ionosphere (IRI) 2016 model. 

It requires [Time Utilities](https://github.com/rilma/TimeUtilities).

### Installing

```
python setup.py install
```

## Examples

### Height-profile
Use this [script](examples/iri1DExample01.py) to generate a plot of density and temperatures vs height:

![alt tag](figures/iri1DExample01.png)

### Latitudinal profile
Use this [script](examples/iri1DExample02.py) to generate a plot of densities and height at the peak of F2, F2, and E regions vs geographic latitude:

![alt tag](figures/iri1DExample02.png)

### GMT profile
Use this [script](examples/iri1DExample08.py) to generate a plot of densities and height at the peak of F2, F2, and E regions vs universal time:

![alt tag](figures/iri1DExample08.png)

### Height vs GMT
Use this [script](scripts/iri2DExample01.py) to generate a plot of Ne, Te, and Ti as a function of height and universal time:

![alt tag](figures/iri2DExample01.png)

### Latitude vs Longitude
Use this [script](scripts/iri2DExample02.py) to generate a plot of foF2 a function of geographic latitude and longitude:

![alt tag](figures/iri2DExample02.png)
