Many Python programs--including IRI2016--are readily accessible from Matlab.
Here's what's you'll need:

1. Python &ge; 3.6.  Check which Python version you have simply by typing from Terminal/Command Prompt (not in Matlab)
   ```sh
   python3
   ```
   If you need to install Python, consider [Miniconda](https://conda.io/miniconda.html) as it's a small install (normally, use the 64-bit version).
2. Matlab &ge; R2017b, as this is when Python 3.6 was enabled. 
   If you're stuck with older Matlab &lt; R2017b, you can try to [force-enable Python 3.6](https://www.scivision.co/matlab-python-user-module-import/)
3. The function [iri2016.m](iri2016.m) gives some examples of what you can do (run, plot) IRI2016 from Matlab calling Python (and ultimately the original Fortran code).
   The functions in that file `xarrayind2vector()` and `xarray2mat()` translate Python's advanced Xarray N-D data structures to Matlab arrays.
