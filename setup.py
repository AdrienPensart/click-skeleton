
# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = ''

setup(
    long_description=readme,
    name='click-skeleton',
    version='0.3.1',
    description='Click app skeleton',
    python_requires='<4.0,>=3.6',
    author='Adrien Pensart',
    packages=['click_skeleton'],
    package_dir={"": "."},
    package_data={},
    install_requires=['click==7.*,>=7.1.2', 'click-aliases==1.*,>=1.0.1', 'click-completion==0.*,>=0.5.0', 'click-didyoumean==0.*,>=0.0.3', 'click-help-colors==0.*,>=0.8.0', 'click-option-group==0.*,>=0.5.1', 'colorama==0.*,>=0.4.3', 'pytest==6.*,>=6.0.1', 'pytest-click==1.*,>=1.0.2'],
    extras_require={"dev": ["pylint==2.*,>=2.6.0", "pytest-cov==2.*,>=2.10.1"]},
)
