#!/usr/bin/env python

from setuptools import setup, find_packages
import access_manager

setup(
    name='django-access-manager',
    version=".".join(map(str, access_manager.__version__)),
    author='Anton Agestam',
    author_email="msn@antonagestam.se",
    url='http://github.com/FundedByMe/django-access-manager',
    install_requires=[
        'Django>=1.4.8',
    ],
    description='An abstract access manager for Django.',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)
