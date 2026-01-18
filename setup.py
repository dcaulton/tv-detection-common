from setuptools import setup

setup(
    name='tv-detection-common',
    version='0.1.0',
    packages=['tv_detection_common'],
    install_requires=['sqlalchemy>=1.4'],
    description='Shared DB models for tv-detection projects'
)
