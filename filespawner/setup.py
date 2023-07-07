#!/usr/bin/env python
from __future__ import print_function

import os
import sys

v = sys.version_info
if v[:2] < (3, 3):
    error = 'ERROR: Jupyter Hub requires Python version 3.3 or above.'
    print(error, file=sys.stderr)
    sys.exit(1)


if os.name in ('nt', 'dos'):
    error = 'ERROR: Windows is not supported'
    print(error, file=sys.stderr)

from distutils.core import setup

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))

setup_args = dict(
    name='filespawner',
    packages=['filespawner'],
    version='0.0.1',
    description='''FileSpawner: A JupyterHub spawner designed for opening a single file''',
    long_description='',
    author='Collin Bolles',
    author_email='cbolles@bu.edu',
    license='ISC',
    platforms='Linux, Mac OS X',
    keywords=['Interactive', 'Interpreter', 'Shell', 'Web', 'Marathon'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)

if 'bdist_wheel' in sys.argv:
    import setuptools

# setuptools requirements
if 'setuptools' in sys.modules:
    setup_args['install_requires'] = install_requires = []
    with open('requirements.txt') as f:
        for line in f.readlines():
            req = line.strip()
            if not req or req.startswith(('-e', '#')):
                continue
            install_requires.append(req)


def main():
    setup(**setup_args)

if __name__ == '__main__':
    main()
