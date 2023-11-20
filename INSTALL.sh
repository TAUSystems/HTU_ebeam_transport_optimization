#!/bin/bash
poetry install
poetry run pip install setuptools wheel pykern
poetry run pip install "rsopt[full] @ git+https://github.com/radiasoft/rsopt@c176a36"
