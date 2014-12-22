#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="python-intis",
      version="0.1",
      description="Intis SMS API client",
      license="MIT",
      install_requires=["six"],
      author="Muhortov Ilya",
      author_email="muhortov@gmail.com",
      url="http://github.com/ilya-muhortov/python-intis",
      packages = find_packages(),
      keywords= "intis",
      zip_safe = True)