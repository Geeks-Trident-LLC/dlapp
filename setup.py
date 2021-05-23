"""Packaging dlquery."""

from setuptools import setup, find_packages
from dlquery import version


setup(
    name='dlquery',
    version=version,
    license='BSD-3-Clause',
    license_files=['LICENSE'],
    description='Python module for querying dictionary or list object.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tuyen Mathew Duong',
    author_email='tuyen@geekstrident.com',
    maintainer='Geeks Trident LLC',
    maintainer_email='tuyen@geekstrident.com',
    install_requires=['pyyaml'],
    url='https://github.com/Geeks-Trident-LLC/dlquery',
    packages=find_packages(
        exclude=(
            'tests*', 'testing*', 'examples*',
            'build*', 'dist*', 'docs*', 'venv*'
        )
    ),
    entry_points={
        'console_scripts': [
            'dlquery-test = dlquery.acceptance:test_acceptance',
            'dlquery = dlquery.main:execute',
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
