"""Packaging dlquery."""

from setuptools import setup, find_packages


setup(
    name='dlquery',
    version='1.0.0',
    license='BSD-3-Clause',
    license_files=['LICENSE'],
    description='Python module for querying dictionary or list object.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tuyen Mathew Duong',
    author_email='tuyen@geekstrident.com',
    maintainer='Geeks Trident LLC',
    maintainer_email='tuyen@geekstrident.com',
    install_requires=['pyyaml', 'compare_versions'],
    url='https://github.com/Geeks-Trident-LLC/dlquery',
    packages=find_packages(
        exclude=(
            'tests*', 'testing*', 'examples*',
            'build*', 'dist*', 'docs*', 'venv*'
        )
    ),
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'dlquery = dlquery.main:execute',
            'dlquery-gui = dlquery.application:execute'
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
