# RSOpt simulation manager
An application to run `rsopt` experiments and manage the simulation runs.

## Install
abcd

## Startup
To start the simulation manager, run

```poetry run python rsopt_simulation_manager/run.py```

Then open the given address, likely http://127.0.0.1:5000/, in a browser.

## Usage
First, use the Settings tab to set the directory where the simulation files are 
and the directory where results should be saved.

The RSOpt simulation files directory should contain `run.sh` which contains the 
command to be run, such as 

```rsopt optimize configuration configuration.yml```, 

as well as all of the required files (e.g. configuration.yml, .lte, .ele, .py files)
to run the RSOpt simulation.

Next, create an Experiment. This represents a collection of similar simulation runs.

Then create a new Run. When you hit "Run simulation", the following happens:
* A run folder of the form \<Results base folder\>/_experiment name_/_datetime_
  will be created
* Files in the RSOpt simulation files directory are copied to \<run folder\>/input 
* The command in `run.sh` is executed,  with the RSOpt simulation files directory 
  as working directory.
* Any generated output that is dumped in the RSOpt simulation files directory (as
  RSOpt doesn't seem to allow specifying a different output folder) is copied to
  \<run folder\>/output


## Credits
This app is based on [Argon Dashboard Flask](https://www.creative-tim.com/product/argon-dashboard-flask)

