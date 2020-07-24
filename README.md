# IRI2016 ionosphere model from Python and Matlab

[![image](https://zenodo.org/badge/DOI/10.5281/zenodo.240895.svg)](https://doi.org/10.5281/zenodo.240895)
![Actions Status](https://github.com/space-physics/iri2016/workflows/ci/badge.svg)
[![codecov](https://codecov.io/gh/space-physics/iri2016/branch/master/graph/badge.svg)](https://codecov.io/gh/space-physics/iri2016)
[![PyPi version](https://img.shields.io/pypi/pyversions/iri2016.svg)](https://pypi.python.org/pypi/iri2016)
[![PyPi Download stats](http://pepy.tech/badge/iri2016)](http://pepy.tech/project/iri2016)


![image](./figures/iri2DExample02.gif)

Python and [Matlab](#matlab) interfaces to the International Reference Ionosphere (IRI) 2016 model.
A Fortran compiler is required to build the IRI2016 code.

## Install

**Prerequisites**

* Fortran compiler--any modern Fortran compiler will do. Here's how to get Gfortran:
  * Linux: `apt install gfortran`
  * Mac: `brew install gcc`
  * Windows: consider [MSYS2](https://www.scivision.dev/install-msys2-windows/)

and then install latest release:

```sh
pip install iri2016
```

if you want the latest development version:

```sh
git clone https://github.com/space-physics/iri2016

pip install -e iri2016
```

This Python wrapper of IRI2016 uses our build-on-run technique.
The first time you use IRI2016, you will see messages from the Meson build system and your C compiler.

If you have errors about building on the first run, ensure that your Fortran compiler is specified in environment variable FC--this is what most build systems use to indicate the desired Fortran compiler (name or full path).

### Manual build

This should not be necessary, but is included for troubleshooting purposes.
This assumess you have a local copy of IRI2016 like:

```sh
git clone https://github.com/space-physics/iri2016

cd iri2016

cmake -S iri2016 -B iri2016/build

cmake --build iri2016/build
```

## Usage

* Altitude Profile: plot density and temperatures vs altitude

  ```sh
  iri2016_altitude 2003-11-21T12 -11.95 -76.77
  ```

  ![image](./figures/iri1DExample01.png)
* Latitude profile: plot densities and height at the peak of F2, F2, and E regions vs geographic latitude

  ```sh
  iri2016_latitude 2004-11-21T17 -76.77
  ```

  ![image](./figures/iri1DExample02.png)
* Time profile: plot densities and height at the peak of F2, F2, and E regions vs UTC

  ```sh
  iri2016_time 2014-11-21 2014-11-22 1 -11.95 -76.77
  ```

  ![image](./figures/plasma.png)

  ![image](./figures/tec.png)

  ![image](./figures/iri2DExample01.png)
* Latitude vs Longitude: plot of foF2 a function of geographic latitude and longitude
  ![image](./figures/iri2DExample02.png)

### setting JF flags

[irisub.for](./iri2016/src/irisub.for) has a few dozen logical flags stored in variable JF. To reconfigure those flags, edit [iri2016_driver.f90](./iri2016/src/iri2016_driver.f90) and recompile iri2016_driver.exe.

### Matlab / GNU Octave

IRI2016 is readily accessible from Matlab and GNU Octave.
From within Matlab / Octave, verify everything is working by from the `iri2016/tests` directory:

```matlab
test_iri2016
```

* [iri2016.m](./matlab/iri2016.m) function accesses IRI2016 quantities.
* [RunIRI2016.m](./matlab/RunIRI2016.m) is a simple example use with plots.

![Matlab IRI2016 plot](./figures/matlab.png)

## Data files

`iri2016/iri2016/data/index/{apf107,ig_rz}.dat` are
[regularly updated](http://irimodel.org/indices/).
Currently we don't auto-update those.

## Notes

* [2016 presentation](https://doi.org/10.5281/zenodo.1493021)
