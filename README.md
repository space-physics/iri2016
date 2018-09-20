[![image](https://zenodo.org/badge/DOI/10.5281/zenodo.240895.svg)](https://doi.org/10.5281/zenodo.240895)
[![Build Status](https://travis-ci.org/scivision/IRI2016.svg?branch=master)](https://travis-ci.org/scivision/IRI2016)
[![image](https://coveralls.io/repos/github/scivision/IRI2016/badge.svg?branch=master)](https://coveralls.io/github/scivision/IRI2016?branch=master)
[![Build status](https://ci.appveyor.com/api/projects/status/euvvim6aus3dagwq?svg=true)](https://ci.appveyor.com/project/scivision/pyiri2016)
[![PyPi version](https://img.shields.io/pypi/pyversions/iri2016.svg)](https://pypi.python.org/pypi/iri2016)
[![PyPi formats](https://img.shields.io/pypi/format/iri2016.svg)](https://pypi.python.org/pypi/iri2016)
[![PyPi Download stats](http://pepy.tech/badge/iri2016)](http://pepy.tech/project/iri2016)


# IRI2016 ionosphere model from Python and Matlab

![image](figures/iri2DExample02.gif)

A Python interface to the International Reference Ionosphere (IRI) 2016 model.

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

    pip install iri2016

or:

    python -m pip install -e .
    
### Windows
If you get ImportError on Windows for the Fortran module, try from the `iri2016` directory:
```posh
del *.pyd
python setup.py build_ext --inplace --compiler=mingw32
```

## Usage

* Height-profile: plot density and temperatures vs [altitude](AltitudeProfile.py)
  ![image](figures/iri1DExample01.png)
* Latitudinal profile: plot densities and height at the peak of F2, F2, and E regions vs [geographic latitude](LatitudeProfile.py)
  ![image](figures/iri1DExample02.png)
* GMT profile: plot densities and height at the peak of F2, F2, and E regions vs universal [time](TimeProfile.py)
  ![image](figures/iri1DExample08.png)
* Height vs GMT: plot Ne, Te, and Ti as a function of height and universal [time](scripts/iri2DExample01.py)
  ![image](figures/iri2DExample01.png)
* Latitude vs Longitude: plot of foF2 a function of geographic latitude and [longitude](scripts/iri2DExample02.py)
  ![image](figures/iri2DExample02.png)
  
### Matlab
Many Python programs--including IRI2016--are readily accessible from Matlab.
Here's what's you'll need:

1. Python &ge; 3.6.  Check which Python version you have simply by typing from Terminal/Command Prompt (not in Matlab)
   ```sh
   python3
   ```
   If you need to install Python, consider [Miniconda](https://conda.io/miniconda.html) as it's a small install (normally, use the 64-bit version).
2. Matlab &ge; R2014b
3. The function [iri2016.m](iri2016.m) gives some examples of what you can do (run, plot) IRI2016 from Matlab calling Python (and ultimately the original Fortran code).
   The functions in that file `xarrayind2vector()` and `xarray2mat()` translate Python's advanced Xarray N-D data structures to Matlab arrays.

## Notes

These commands are not normally needed unless you want to work with the Fortran code more directly.

### Fortran compile

    cd bin
    cmake ../fortran

    cmake --build .

    ctest -V

### f2py compile

The function DFRIDR() inside igrf.for dynamically calls other functions.
This is something f2py can't access directly, so we tell f2py not to
hook into function DFRIDF() with the end statement `skip: dfridr`:

    f2py -m iri2016 -c iriwebg.for irisub.for irifun.for iritec.for iridreg.for igrf.for  cira.for iriflip.for  skip: dfridr

### f2py: IGRF only

    f2py -m igrf -c irifun.for igrf.for skip: dfridr
