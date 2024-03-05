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
installs `rsopt`

## RSOpt Simulation Manager
Please see [resopt_simulation_manager/README.md](rsopt_simulation_manager/README.md) 
for full instructions. But to get started: 

1. Start the simulation manager with `poetry run python rsopt_simulation_manager/run.py` 
   and open the given address in a browser.
1. Set the RSOpt files and results directories in Settings
1. Create an Experiment 
1. Start a Run 
