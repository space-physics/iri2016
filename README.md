[![image](https://zenodo.org/badge/DOI/10.5281/zenodo.240895.svg)](https://doi.org/10.5281/zenodo.240895)

[![Actions Status](https://github.com/space-physics/iri2016/workflows/ci/badge.svg)](https://github.com/space-physics/iri2016/actions)

[![PyPi version](https://img.shields.io/pypi/pyversions/iri2016.svg)](https://pypi.python.org/pypi/iri2016)
[![PyPi Download stats](http://pepy.tech/badge/iri2016)](http://pepy.tech/project/iri2016)


# IRI2016 ionosphere model from Python and Matlab

![image](./figures/iri2DExample02.gif)

Python and [Matlab](#matlab) interfaces to the International Reference Ionosphere (IRI) 2016 model.
A Fortran compiler and CMake or
[Meson](https://github.com/mesonbuild/meson/)
is required to build the IRI2016 code.

## Install

**Prerequisites**

* Python >= 3.6
* Ninja-build obtained by:
  * Linux: `apt install ninja-build`
  * MacOS/Homebrew: `brew install ninja`
  * Windows Chocolatey: `cinst -y ninja`
  * [direct download](https://github.com/ninja-build/ninja/releases) and extract, put directory in PATH environment variable.
* Fortran compiler--just about any modern Fortran compiler will do. Here's how to get Gfortran:
  * Linux: `apt install gfortran`
  * Mac: `brew install gcc`
  * [Windows](https://www.scivision.dev/windows-gcc-gfortran-cmake-make-install/)

and then install latest release:

```sh
pip install iri2016
```

if you want the latest development version:

```sh
git clone https://github.com/space-physics/iri2016

pip install -e iri2016
```

## Usage

* Altitude Profile: plot density and temperatures vs altitude

  ```sh
  python AltitudeProfile.py 2003-11-21T12 -11.95 -76.77
  ```

  ![image](./figures/iri1DExample01.png)
* Latitude profile: plot densities and height at the peak of F2, F2, and E regions vs geographic latitude

  ```sh
  python LatitudeProfile.py 2004-11-21T17 -76.77
  ```

  ![image](./figures/iri1DExample02.png)
* Time profile: plot densities and height at the peak of F2, F2, and E regions vs UTC

  ```sh
  python TimeProfile.py 2014-11-21 2014-11-22 1 -11.95 -76.77
  ```

  ![image](./figures/iri1DExample08.png)

  ![image](./figures/iri2DExample01.png)
* Latitude vs Longitude: plot of foF2 a function of geographic latitude and longitude
  ![image](./figures/iri2DExample02.png)

### Matlab / GNU Octave
IRI2016 is readily accessible from Matlab and GNU Octave.
From within Matlab/Octave, verify everything is working by from the `iri2016/tests` directory:

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
