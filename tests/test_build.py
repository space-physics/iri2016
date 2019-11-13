#!/usr/bin/env python
import pytest
import iri2016.build as build
from pathlib import Path

R = Path(__file__).parent.resolve()


@pytest.mark.parametrize("build_sys", ["cmake", "meson"])
def test_build(build_sys, tmp_path):
    if build_sys == "cmake" and not build.check_cmake_version("3.13"):
        pytest.skip("Too old CMake")

    build.build(build_sys, R.parent, tmp_path)


def test_bad(tmp_path):
    with pytest.raises(ValueError):
        build.build("fake", R.parent, tmp_path)


if __name__ == "__main__":
    pytest.main([__file__])
