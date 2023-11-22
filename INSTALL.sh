#!/bin/bash

# create virtual environment and install dependencies from pyproject.toml
poetry install

# install rsopt into virtual environment. This must be done separately because
# pykern needs to be available to build rsopt
poetry run pip install "rsopt[full] @ git+https://github.com/radiasoft/rsopt@c176a36"

# revert sirepo (installed by rsopt) to an older version that doesn't require pymoab 
# and pymeshlab
poetry run pip install "sirepo @ git+https://github.com/radiasoft/sirepo.git@013784b70e06fa27f9f346d557a659bf99e4f850"
