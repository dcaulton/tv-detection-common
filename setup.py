from setuptools import setup, find_packages

setup(
    name='tv-detection-common',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['sqlalchemy'],
    description='Shared DB models for tv-detection projects'
)
