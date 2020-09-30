#!/usr/bin/env python3
import setuptools
import site

# PEP517 workaround
site.ENABLE_USER_SITE = True

setuptools.setup()

"""
Because of bugs in IRI2016 itself, present even in plain Fortran usage, we can't safely use F2py, bad data can result.
"""
