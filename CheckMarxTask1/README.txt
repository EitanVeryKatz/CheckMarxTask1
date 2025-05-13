# PyPI Dependency Analyzer

A Python-based utility to analyze the latest version of a given PyPI package by:
- Fetching its latest version from PyPI
- Downloading the package archive (`.whl` or `.tar.gz`)
- Extracting the package files
- Parsing metadata (e.g., `setup.py`, `install_requires`, `requirements.txt`)
- Returning a structured list of dependencies

## Features

- Supports `.whl` and `.tar.gz` formats
- Handles missing files and network errors gracefully
- Modular, testable design
- Can be used as a library or standalone tool


#usage 

__init__.py contains the high level function for retrieval of the dependencies of the wanted package.

test.py contains module that uses that function by requesting package name as user input and printing to the console 
the dependencies list for that package