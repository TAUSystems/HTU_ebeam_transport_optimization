#!/bin/bash

# create virtual environment and install dependencies from pyproject.toml
poetry install

# install rsopt into virtual environment. This must be done separately because
# pykern needs to be available to build rsopt
# rsopt automatical installs sirepo, but there seems to be an issue with the currrent version
# code below is a hacky way to install a functional verion of sirepo from 2024-01-25

poetry run pip install "rsopt[full] @ git+https://github.com/radiasoft/rsopt"
poetry run pip uninstall sirepo -y
poetry run pip install "sirepo @ git+https://github.com/radiasoft/sirepo@bad43d1d5916c399f99bd89e70017c66cc459b23"


