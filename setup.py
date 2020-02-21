from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

setup(
    name='M2B_ETL', 
    version='1.3.1', 
    packages=find_packages(where='egress') + find_packages(where='connection') + find_packages(where='extract')+find_packages(where='provisioning'),  # Required
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
)