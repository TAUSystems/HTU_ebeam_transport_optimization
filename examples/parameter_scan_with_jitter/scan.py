import yaml
import subprocess
from pathlib import Path

def add_or_modify_yaml_parameter(file_path, parameter_path, parameter_values):
    """
    Add or modify a parameter in the YAML file under 'parameters'.
    
    Parameters:
    - file_path: Path to the YAML file.
    - parameter_path: Path to the parameter (e.g., ['codes', 'elegant', 'parameters', 'EMQ3H.K1']).
    - parameter_values: A dictionary of the parameter attributes to add or modify (e.g., {'max': 20, 'min': -20, 'samples': 1, 'start': 9.7}).
    """
    with open(file_path) as f:
        data = yaml.safe_load(f)
    
    temp = data
    for index, key in enumerate(parameter_path[:-1]):
        if isinstance(temp, list):  # Check if current node is a list
            # Assuming the structure under 'codes' and that we're targeting the first item
            if key == 'codes' and index == 0:  # 'codes' is expected to be the first in the path
                temp = temp[0]  # Access the first item for 'codes'
            else:
                # This else block is to handle other potential list accesses, adapt as necessary
                print("Error: Unhandled list encountered in the path")
                return
        else:
            if key not in temp:
                temp[key] = {}
            temp = temp[key]

    # Assign the new or modified parameter values
    temp[parameter_path[-1]] = parameter_values
    
    with open(file_path, 'w') as f:
        yaml.safe_dump(data, f, default_flow_style=False)

def run_simulation_and_summary(yaml_file, setting_path, values):
    """
    Run simulation and summary for a range of values for a specific setting in the YAML file.
    Passes the current setting value as an argument to summary.py.
    
    Parameters:
    - yaml_file: Path to the YAML configuration file.
    - setting_path: Path to the setting in the YAML file to vary (as a list of keys).
    - values: A list of values to set for the specified setting.
    """
    for value in values:
        # Modify the YAML file for the current value
        add_or_modify_yaml_parameter(yaml_file, setting_path, {'start': value})
        
        # Run rsopt command
        subprocess.run(['rsopt', 'sample', 'configuration', yaml_file], check=True)
        
        # Run summary.py script with the current setting value as an argument
        subprocess.run(['python', 'summary.py', str(value)], check=True)

# Example usage
yaml_file = 'single_sim_with_jitter.yml'
scan_parameter_name = 'EMQ3H.K1'
parameter_path = ['codes', 'elegant', 'parameters', scan_parameter_name]  # Corrected variable name

# Initial parameter values (Not used directly in the example but shown for completeness)
parameter_values = {
    'max': 20,
    'min': -20,
    'samples': 1,
    'start': 9.7
}

values = [7.7, 8.2, 8.7, 9.2, 9.7, 10.2, 10.7]  # Example values to loop through

# Correctly define setting_path for use
setting_path = parameter_path  # Here setting_path and parameter_path refer to the same

run_simulation_and_summary(yaml_file, setting_path, values)
