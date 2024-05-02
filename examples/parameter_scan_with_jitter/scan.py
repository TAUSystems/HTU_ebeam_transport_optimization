import yaml
import subprocess
from pathlib import Path

def add_or_modify_yaml_parameter(file_path, parameter_path, value):
    """
    Add or modify a parameter in the YAML file under 'parameters'.
    
    Parameters:
    - file_path: Path to the YAML file.
    - parameter_path: Path to the parameter (e.g., ['codes', 'elegant', 'parameters', 'EMQ3H.K1']).
    - value: the value to set the parameter to).
    """
    with open(file_path) as f:
        data = yaml.safe_load(f)
    
    temp = data
    print(data)
    print(data['codes'][0]['elegant']['parameters'])

    if parameter_path[-1] in temp['codes'][0]['elegant']['parameters']:
        del temp['codes'][0]['elegant']['parameters'][parameter_path[-1]]
        
    temp['codes'][0]['elegant']['parameters'][parameter_path[-1]] = parameter_values
    temp['codes'][0]['elegant']['parameters'][parameter_path[-1]]['start'] = value
    
    #     # Assign the new or modified parameter values
    # else:
    #     print('scan parameter already in file. remvoe and try again')
    
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
        add_or_modify_yaml_parameter(yaml_file, setting_path, value)
        
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
