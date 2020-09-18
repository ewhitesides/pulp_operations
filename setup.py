"""
setup config
"""
from setuptools import setup, find_packages

setup(
    name='pulp_operations',
    version='1.0',
    author='Erik Whitesides',
    author_email='ekw45@georgetown.edu',
    description='tool to perform various tasks on pulp server',
    url='https://gitlab.uis.georgetown.edu/devops/pulp_operations',
    packages=find_packages(),
    install_requires=[
        'pulpcore-client>=3.6.1',
        'pulp-rpm-client>=3.6.1'
    ],
    zip_safe=False
)
