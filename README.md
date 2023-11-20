# HTU_ebeam_transport_quadrupole_optimization
Use elegant and GEECS-PythonAPI to optimize electro- and permanent quadrupole magnets in BELLA HTU's electron beam transport system.

## Install
This project uses `rsopt`, which uses `pykern` to install it. Since this doesn't
play well with the `pyproject.toml` paradigm, the `pyproject.toml` contains 
all dependencies except `rsopt`, which then needs to be installed afterward. 

### Poetry
If using `poetry` (preferred), `rsopt` needs to be installed into the virtual
environment created by `poetry` after the other dependencies, because it's not
possible (afaik) for poetry to provide `rsopt`'s build dependency `pykern`. 

The easiest way[^1] to do this is as follows:
1. Navigate to the directory containing this README.
1. Run `poetry install`
1. Run `poetry run pip install setuptools wheel pykern`
1. Run `poetry run pip install "rsopt[full] @ git+https://github.com/radiasoft/rsopt"`

This sequence is listed in `INSTALL.sh`, with the addition of a specific `rsopt`
commit.

[^1] The slightly cleaner way is to build a wheel of `rsopt` in a virtual environment 
and install the resulting wheel into the `poetry` environment. 
