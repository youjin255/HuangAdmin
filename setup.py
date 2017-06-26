#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# requirements
install_requires = [
    "Flask==0.11.1",
    "SQLAlchemy==1.0.14",
    "Jinja2==2.8",
]

setup(name="huangadmin",
      version=__import__("huangadmin").__version__,
      description="Admin For Flask",
      author="huang",
      author_email="jiantao19993@gmail.com",
      packages=find_packages(),
      url="https://github.com/JiangTao11/HuangAdmin.git",
      install_requires=install_requires)
