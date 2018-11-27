[![image](https://zenodo.org/badge/DOI/10.5281/zenodo.240895.svg)](https://doi.org/10.5281/zenodo.240895)
[![Build Status](https://travis-ci.org/scivision/IRI2016.svg?branch=master)](https://travis-ci.org/scivision/IRI2016)
[![image](https://coveralls.io/repos/github/scivision/IRI2016/badge.svg?branch=master)](https://coveralls.io/github/scivision/IRI2016?branch=master)
[![Build status](https://ci.appveyor.com/api/projects/status/euvvim6aus3dagwq?svg=true)](https://ci.appveyor.com/project/scivision/pyiri2016)
[![PyPi version](https://img.shields.io/pypi/pyversions/iri2016.svg)](https://pypi.python.org/pypi/iri2016)
[![PyPi Download stats](http://pepy.tech/badge/iri2016)](http://pepy.tech/project/iri2016)


# IRI2016 ionosphere model from Python and Matlab

![image](./figures/iri2DExample02.gif)

Python and [Matlab](#matlab) interfaces to the International Reference Ionosphere (IRI) 2016 model.

## Python

1. Install IRI2016 command-line driver program
   ```sh
   pip install -e .[tests]
   ```
2. run selftest to ensure install was completed:
   ```sh
   pytest
   ```
3. try example script e.g. [AltitudeProfile.py](./AltitudeProfile.py)

## Matlab

1. compile Fortran code via [matlab/setup_iri2016.m](./matlab/setup_iri2016.m)
2. drive the simulation via a seamless command line interface, example: [matlab/RunIRI2016.m](./matlab/RunIRI2016.m)



## Compiler

Any Fortran compiler will do. 
IRI2016 has been tested with compilers including:

* Gfortran 4.8, 5, 6, 7, 8
* Intel `ifort`
* PGI `pgf90`
* Flang `flang`

If you don't already have a Fortran compiler, install Gfortran by:

* Linux: `apt install gfortran`
* Mac: `brew install gcc`
* [Windows](https://www.scivision.co/windows-gcc-gfortran-cmake-make-install/)

    
## Usage

* Height-profile: plot density and temperatures vs [altitude](./AltitudeProfile.py)
  ![image](./figures/iri1DExample01.png)
* Latitudinal profile: plot densities and height at the peak of F2, F2, and E regions vs [geographic latitude](./LatitudeProfile.py)
  ![image](./figures/iri1DExample02.png)
* GMT profile: plot densities and height at the peak of F2, F2, and E regions vs universal [time](./TimeProfile.py)
  ![image](./figures/iri1DExample08.png)
* Height vs GMT: plot Ne, Te, and Ti as a function of height and universal [time](./examples/example01.py)
  ![image](./figures/iri2DExample01.png)
* Latitude vs Longitude: plot of foF2 a function of geographic latitude and [longitude](./examples/example02.py)
  ![image](./figures/iri2DExample02.png)
  
### Matlab / GNU Octave
IRI2016 is readily accessible from Matlab and GNU Octave.

1. From Matlab, verify everything is working by from the `iri2016/` directory:
   ```matlab
   runtests('tests')
   ```
2. Use [iri2016.m](./matlab/iri2016.m) function to access IRI2016 quantities.  See [RunIRI2016.m](./matlab/RunIRI2016.m) for simple example use / plots.

![Matlab IRI2016 plot](./figures/matlab.png)

## Data files

`iri2016/iri2016/data/index/{apf107,ig_rz}.dat` are 
[regularly updated](http://irimodel.org/indices/).
Currently we don't auto-update those.

## Direct compilation

These commands are not normally needed unless you want to work with the Fortran code more directly.

### Fortran compile

```sh
cd bin
cmake ../src

cmake --build .

ctest -V
```

## Notes

* [2016 presentation](https://doi.org/10.5281/zenodo.1493021)
