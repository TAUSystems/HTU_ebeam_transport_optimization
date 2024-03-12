import yaml
import subprocess
from pathlib import Path

import os
import time
import numpy as np
import pandas as pd
import shelve
import sys

from xopt.evaluator import Evaluator
from xopt.generators.bayesian import ExpectedImprovementGenerator
from xopt import Xopt
import random


import torch

from shared.optimization_functions import visa1_4_size_min

step_number = 0

def run_simulation_and_summary(yaml_file, changes):
    """
    Run simulation and summary for a range of values for a specific setting in the YAML file.
    Passes the cahnges as an argument to summary.py.
    
    Parameters:
    - yaml_file: Path to the YAML configuration file.
    - changes: Dictionary of changes to apply to the YAML file.
    - iteration: The current iteration number.
    """
    
    global step_number
    update_parameters(yaml_file, changes)
    
    iteration = step_number
    
    print('iteration: ',iteration)
    
    # Run rsopt command
    subprocess.run(['rsopt', 'sample', 'configuration', yaml_file], check=True)

    sim_directory = f'iteration_{iteration}'

    # Run summary.py script with the current setting value as an argument
    subprocess.run(['python', 'summary.py', sim_directory], check=True)
    
    return sim_directory
        
def update_parameters(yaml_file, changes, default_min=-10, default_max=10, default_samples=1):
    """
    Updates the start values of parameters in a YAML file. Adds new parameters with default values if they do not exist.

    :param yaml_file: Path to the YAML file.
    :param changes: A dictionary where keys are parameter names and values are the new start values.
    :param default_min: Default minimum value for new parameters.
    :param default_max: Default maximum value for new parameters.
    :param default_samples: Default samples value for new parameters.
    """
    
    with open(yaml_file) as file:
        data = yaml.safe_load(file)

    # Assuming the structure always contains 'codes' and we target the first item under 'codes'
    for key, new_start in changes.items():
        parameters = data['codes'][0]['elegant']['parameters']
        if key in parameters:
            parameters[key]['start'] = new_start
        else:
            parameters[key] = {
                'min': default_min,
                'max': default_max,
                'samples': default_samples,
                'start': new_start
            }

    with open(yaml_file, 'w') as file:
        yaml.safe_dump(data, file)

def simulation_optimize(input_dict,iteration=0):
    sim_directory = run_simulation_and_summary(yaml_file, input_dict)
    function_value = visa1_4_size_min.obj_f(sim_directory)
    print('input dict: ',input_dict)
    print('Target dict: ',function_value)
    return {"f":function_value}


def load_xopt_base_config(filename: str = "bayes_ucb", directory: str = "config_files/base_xop_optimization_configs") -> dict:
    """
    Loads an xopt yaml config from a given directory based on the filename.

    Args:
    - filename (str): The name of the file without the .yaml extension. Default is "bayes_ucb".
    - directory (str): The directory where the yaml file is located. Default is "config_files/base_xop_optimization_configs".

    Returns:
    - dict: The parsed data from the yaml file.
    """

    with open(os.path.join(directory, f"{filename}.yaml"), 'r') as file:
        data = yaml.safe_load(file)
    return data
    
def generate_random_vocs_values(data):
    # with open(yaml_file, 'r') as file:
    #     data = yaml.safe_load(file)

    # Extracting the 'variables' dictionary from the YAML content
    variables = data['vocs']['variables']
    
    # Generating a new dictionary with random values within the defined ranges
    random_values = {var: [random.uniform(min_val, max_val)] for var, (min_val, max_val) in variables.items()}
    
    return random_values

def initialize_xopt():
    global step_number
    yaml_config = load_xopt_base_config()
    yaml_string = yaml.dump(yaml_config)
    print(yaml_string)
    X = Xopt.from_yaml(yaml_string)
    # print(X)
    
    # print initial number of points to be generated
    n_initial=1
    for i in range(n_initial):
        step_number = step_number + 1
        random_vocs_values = generate_random_vocs_values(yaml_config)
        random_vocs_values = {'EMQ1H.K1':[6.28],'EMQ2V.K1':[-7.78],'EMQ3H.K1':[9.8],}
        print('random_vocs_values: ',random_vocs_values)
        X.evaluate_data(random_vocs_values)
    print('optimization initialized')
    
    return X
    
def xopt_step(X):
    global step_number
    step_number = step_number + 1
    try:
        # Attempt to execute code that might raise an exception
        X.step()
    except Exception as e:
        # Handle exceptions
        print(f"An error occurred during optimization step: {e}")
        # Optionally, return a default value or re-raise the exception
        return None  # or raise e

# Example usage

yaml_file = 'single_sim_with_jitter.yml'  
# xopt_config_yaml = 'bayes_UCB.yaml'  # Path to your YAML file

X = initialize_xopt()

num_steps = 37
for i in range(num_steps):
    xopt_step(X)


# # Example usage
# yaml_file = 'single_sim_with_jitter.yml'
# scan_parameter_name = 'EMQ3H.K1'
# parameter_path = ['codes', 'elegant', 'parameters', scan_parameter_name]  # Corrected variable name
#
# # Initial parameter values (Not used directly in the example but shown for completeness)
# parameter_values = {
#     'max': 20,
#     'min': -20,
#     'samples': 1,
#     'start': 9.7
# }
#
# values = [7.7, 8.2, 8.7, 9.2, 9.7, 10.2, 10.7]  # Example values to loop through
#
# # Correctly define setting_path for use
# setting_path = parameter_path  # Here setting_path and parameter_path refer to the same
#
# run_simulation_and_summary(yaml_file, setting_path, values)
