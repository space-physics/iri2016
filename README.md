[![image](https://zenodo.org/badge/DOI/10.5281/zenodo.240895.svg)](https://doi.org/10.5281/zenodo.240895)
[![Build Status](https://travis-ci.org/scivision/IRI2016.svg?branch=master)](https://travis-ci.org/scivision/IRI2016)
[![image](https://coveralls.io/repos/github/scivision/IRI2016/badge.svg?branch=master)](https://coveralls.io/github/scivision/IRI2016?branch=master)
[![Build status](https://ci.appveyor.com/api/projects/status/euvvim6aus3dagwq?svg=true)](https://ci.appveyor.com/project/scivision/pyiri2016)
[![PyPi version](https://img.shields.io/pypi/pyversions/iri2016.svg)](https://pypi.python.org/pypi/iri2016)
[![PyPi Download stats](http://pepy.tech/badge/iri2016)](http://pepy.tech/project/iri2016)


# IRI2016 ionosphere model from Python and Matlab

![image](./figures/iri2DExample02.gif)

Python and [Matlab](#matlab) interfaces to the International Reference Ionosphere (IRI) 2016 model.

## Install

Any Fortran compiler will do. 
IRI2016 has been tested with compilers including:

* Gfortran 5, 6, 7, 8
* Intel `ifort`
* PGI `pgf90`

Install Gfortran by:

-   Linux: `apt install gfortran`
-   Mac: `brew install gcc`
-   [Windows](https://www.scivision.co/windows-gcc-gfortran-cmake-make-install/)

and then from your Python &ge; 3.6 install (such as [Miniconda](https://conda.io/miniconda.html)):

```sh
pip install iri2016
```

or:
```sh
git clone https://github.com/scivision/iri2016
cd iri2016

python -m pip install -e .[tests]
```
    
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
  
### Matlab
Many Python programs--including IRI2016--are readily accessible from Matlab.
Here's what's you'll need:

1. [Setup Python &harr; Matlab interface](https://www.scivision.co/matlab-python-user-module-import/).
2. Install IRI2016 in Python as at the top of this Readme.
3. From Matlab, verify everything is working by from the `iri2016/` directory:
   ```matlab
   runtests('tests')
   ```
4. Use [iri2016.m](./matlab/iri2016.m) function to access IRI2016 quantities.  See [RunIRI2016.m](./matlab/RunIRI2016.m) for simple example use / plots.

CAVEAT: due to old-fashioned Fortran 77 techniques, Matlab needs to be restarted to run more than one IRI2016 scenario.
This is also true of the Fortran code itself, and Python.
What we do in Python is call a Python script over and over, inputting distinct parameters.
This can be done from Matlab like the [BatchIRI2016.m](./matlab/BatchIRI2016.m) script, enhanced to call an easier/faster Python script.
Let us know.

![Matlab IRI2016 plot](./figures/matlab.png)

## Direct compilation

These commands are not normally needed unless you want to work with the Fortran code more directly.

### Fortran compile

```sh
cd bin
cmake ../fortran

cmake --build .

ctest -V
```

### f2py compile

The function DFRIDR() inside igrf.for dynamically calls other functions.
This is something f2py can't access directly, so we tell f2py not to
hook into function DFRIDF() with the end statement `skip: dfridr`:

```sh
f2py -m iri2016 -c iriwebg.for irisub.for irifun.for iritec.for iridreg.for igrf.for  cira.for iriflip.for  skip: dfridr
```

### f2py: IGRF only

```sh
f2py -m igrf -c irifun.for igrf.for skip: dfridr
```

## Notes

* [2016 presentation](https://doi.org/10.5281/zenodo.1493021)
