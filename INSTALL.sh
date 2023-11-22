#!/bin/bash

# create virtual environment and install dependencies from pyproject.toml
poetry install

# install rsopt into virtual environment. This must be done separately because
# pykern needs to be available to build rsopt
# rsopt@develop 2023-11-21
poetry run pip install "rsopt[full] @ git+https://github.com/radiasoft/rsopt@76ab6211eed33675eda91930666a0e83d96f568c"
