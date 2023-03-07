#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = [ ]

setup(
    author="Mohammed Salim Dason",
    author_email='salimdason@outlook.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="CLI application for management of versioned Wasabi S3 buckets",
    entry_points={
        'console_scripts': [
            'wasabicli=wasabicli.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='wasabicli',
    name='wasabicli',
    packages=find_packages(include=['wasabicli', 'wasabicli.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/salimdason/wasabicli',
    version='3.0.2',
    zip_safe=False,
)
