import sys
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "wbs_core",
        ["wbs_core/eom.cpp"],
        # Example: passing in compiler flags
        cxx_std=11,
    ),
]

setup(
    name="wilson-ballistic-suite",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False
)
