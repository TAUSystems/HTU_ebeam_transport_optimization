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

The `INSTALL.sh` script creates the environment and its dependencies, and it 
installs `rsopt` and reverts `sirepo` to an older version. See the script for
details.
