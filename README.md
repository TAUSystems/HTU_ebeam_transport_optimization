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
### Startup
To start the simulation manager, run

```poetry run python rsopt_simulation_manager run.py```

Then open the given address, likely http://127.0.0.1:5000/, in a browser.

### Usage
First, use the Settings tab to set the directory where the simulation files are 
and the directory where results should be saved.

Create a new Experiment, which represents a collection of similar simulation runs.

Then create a new Run. When you hit "Run simulation", the following command will
be called from the directory specified by the simulation files directory in Settings:

```rsopt optimize configuration configuration.yml```

So make sure that your configuration is stored in the configuration.yml file.

