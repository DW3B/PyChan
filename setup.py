from setuptools import setup, find_packages

version = "0.0.3"

setup(
    name="pychan",
    version=version,
    description="read-only API wrapper for 4chan.",
    long_description=open("README.md").read(),
    author="DW3B",
    author_email="dweb@dw3b.io",
    license="MIT",
    url="https://github.com/DW3B/PyChan",
    packages=find_packages(),
)
