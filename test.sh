#!/bin/bash

# Run pytest
pytest

# Run black
black .

# Run flake8
flake8 .

# Run isort
isort .

# Run mypy
mypy .

# Blockchain connection tests
# (Assuming you have a separate script or command to run blockchain tests)\nbc_test_script.sh