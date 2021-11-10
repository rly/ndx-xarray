# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages
from shutil import copy2

# load README.md/README.rst file
try:
    if os.path.exists('README.md'):
        with open('README.md', 'r') as fp:
            readme = fp.read()
            readme_type = 'text/markdown; charset=UTF-8'
    elif os.path.exists('README.rst'):
        with open('README.rst', 'r') as fp:
            readme = fp.read()
            readme_type = 'text/x-rst; charset=UTF-8'
    else:
        readme = ""
except Exception:
    readme = ""

setup_args = {
    'name': 'ndx-xarray',
    'version': '0.1.0',
    'description': 'NWB extension to add support for storing/referencing external xarray files',
    'long_description': readme,
    'long_description_content_type': readme_type,
    'author': 'Ryan Ly',
    'author_email': 'rly@lbl.gov',
    'url': 'https://github.com/rly/ndx-xarray',
    'license': 'BSD 3-Clause',
    'install_requires': [
        'pynwb>=2.0.0',
        'hdmf>=3.1.1',
        'xarray>=0.19.0'
    ],
    'packages': find_packages('src/pynwb', exclude=['tests']),
    'package_dir': {'': 'src/pynwb'},
    'package_data': {'ndx_xarray': [
        'spec/ndx-xarray.namespace.yaml',
        'spec/ndx-xarray.extensions.yaml',
    ]},
    'classifiers': [
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    'zip_safe': False
}


def _copy_spec_files(project_dir):
    ns_path = os.path.join(project_dir, 'spec', 'ndx-xarray.namespace.yaml')
    ext_path = os.path.join(project_dir, 'spec', 'ndx-xarray.extensions.yaml')

    dst_dir = os.path.join(project_dir, 'src', 'pynwb', 'ndx_xarray', 'spec')
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)

    copy2(ns_path, dst_dir)
    copy2(ext_path, dst_dir)


if __name__ == '__main__':
    _copy_spec_files(os.path.dirname(__file__))
    setup(**setup_args)
