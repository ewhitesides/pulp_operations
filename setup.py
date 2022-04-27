"""
setup config
"""
from setuptools import setup, find_packages

setup(
    name="pulp_operations",
    version="3.12.2",
    author="Erik Whitesides",
    author_email="eklevjer@gmail.com",
    description="tool to perform various tasks on pulp server",
    url="https://github.com/ewhitesides/pulp_operations",
    packages=find_packages(),
    install_requires=[
        "pulpcore-client==3.12.2",
        "pulp-rpm-client==3.11.1",
        "python-dotenv==0.17.0",
    ],
    zip_safe=False,
)
