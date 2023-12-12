import os
from collections import OrderedDict
import imageio
import numpy as np
from scipy import ndimage
import yaml
import json
import csv



#dict for screens, their sizes, and resolution
screens_dict = OrderedDict({'TCPhosphor':[.01,.000037],"ChicaneSlit":[.01,.00003378],"DCPhosphor":[0.01,.0000168],
                'Phosphor1':[.01,.0000165],"Aline1":[.01,.00002217],"Aline2":[0.01,.00002394],
                'Aline3':[.01,.0000244],"VisaEBeam1":[.0015,.00000755],"VisaEBeam2":[0.0015,.00000755],
                'VisaEBeam3':[.0015,.00000752],"VisaEBeam4":[.0015,.00000741],"VisaEBeam5":[0.0015,.00000768],
                'VisaEBeam6':[.0015,.00000763],"VisaEBeam7":[.0015,.00000735],"VisaEBeam8":[0.0015,.00000707]
                })

def convert_path_to_number(path):
    # Split the string at the space character
    parts = path.split()

    # Check if there are at least two parts
    if len(parts) >= 2:
        # Get the part with the number (e.g., '11p8')
        number_part = parts[-1]

        # Replace 'p' with a dot and convert to a float
        converted_number = float(number_part.replace('p', '.'))

        return converted_number
    else:
        raise ValueError("Invalid path format")

def gather_paths(root_directory, root_name, extension):
    file_paths = []
    quad_vals = []

    # List immediate subdirectories
    subdirectories = [entry.path for entry in os.scandir(root_directory) if entry.is_dir()]

    for subdirectory in subdirectories:
        quad_val=convert_path_to_number(subdirectory)
        quad_vals.append(quad_val)
        for filename in os.listdir(subdirectory):
            if filename.startswith(root_name) and filename.endswith(extension):
                file_paths.append(os.path.join(subdirectory, filename))

    return file_paths, quad_vals
    
    
    

# Calculate FWHM for horizontal and vertical sums
def fwhm(data):
    half_max = np.max(data) / 2.0
    indices = np.where(data >= half_max)[0]
    return indices[-1] - indices[0]

def calculate_image_statistics(image_path):
    # Load the image using imageio
    image = imageio.imread(image_path)

    # Calculate the vertical and horizontal sums using NumPy
    vertical_sum = np.sum(image, axis=0)  # Vertical sum
    horizontal_sum = np.sum(image, axis=1)  # Horizontal sum
    # Calculate the total counts in the image
    total_counts = np.sum(image)
    
    if total_counts == 0:
        centroid_horizontal = 0
        centroid_vertical = 0
        horizontal_rms = 0
        vertical_rms = 0
        fwhm_horizontal = 0
        fwhm_vertical = 0
        
    else:
        # Calculate the center of mass (centroid) for horizontal and vertical sums
        centroid_horizontal = np.average(np.arange(len(horizontal_sum)), weights=horizontal_sum)-len(horizontal_sum)/2.
        centroid_vertical = np.average(np.arange(len(vertical_sum)), weights=vertical_sum)-len(vertical_sum)/2.

        # Calculate the second moment for horizontal and vertical sums
        second_moment_horizontal = np.average((np.arange(len(horizontal_sum)) - centroid_horizontal) ** 2, weights=horizontal_sum)
        horizontal_rms = np.sqrt(second_moment_horizontal)
        second_moment_vertical = np.average((np.arange(len(vertical_sum)) - centroid_vertical) ** 2, weights=vertical_sum)
        vertical_rms = np.sqrt(second_moment_vertical)

        fwhm_horizontal = int(fwhm(horizontal_sum))
        fwhm_vertical = int(fwhm(vertical_sum))

    # Return the calculated statistics as a dictionary
    statistics = {
        "centroid_x": float(centroid_horizontal),
        "centroid_y": float(centroid_vertical),
        "rms_x": float(horizontal_rms),
        "rms_y": float(vertical_rms),
        "fwhm_x": int(fwhm_horizontal),
        "fwhm_y": int(fwhm_vertical),
        'sum_counts': int(total_counts)
    }

    return statistics
    
def calculate_all_image_statistics(root_directory, extension):

    # Create a dictionary to store image statistics for each root name
    image_stats_dict = {}

    # Loop over the root names and calculate statistics for each
    for root_name, _ in screens_dict.items():
        # Use gather_paths to find file paths for the current root name
        file_paths, quad_vals = gather_paths(root_directory, root_name, extension)

        # Check if any matching files were found
        if file_paths:
            for root_name, quad_val in screens_dict.items():
                # Use gather_paths to find file paths and quad_vals for the current root name
                file_paths, quad_vals = gather_paths(root_directory, root_name, extension)

                # Check if any matching files were found
                if file_paths:
                    # Initialize an empty dictionary for the current root_name if it doesn't exist
                    if root_name not in image_stats_dict:
                        image_stats_dict[root_name] = {}

                    # Loop over all found file paths and their corresponding quad_vals
                    for image_path, quad_val in zip(file_paths, quad_vals):
                        # Calculate image statistics for the current file path
                        image_stats = calculate_image_statistics(image_path)

                        # Add quad_val and quad_name to image_stats
                        image_stats['quad_val'] = quad_val
                        image_stats['quad_name'] = "EMQ3"  # To do: extract this programatically

                        # Store the statistics in the nested dictionary
                        image_stats_dict[root_name][quad_val] = image_stats
            
            
    # Serialize and save as YAML
    with open(os.path.join(root_directory, 'image_stats.yaml'), 'w') as yaml_file:
        yaml.dump(image_stats_dict, yaml_file)
        
    # Serialize and save as JSON
    json_data = json.dumps(image_stats_dict, indent=4)
    with open(os.path.join(root_directory,'image_stats.json'), 'w') as json_file:
        json_file.write(json_data)  # Use write() to write the JSON data
        
    data_list = convert_stats_dict_to_list(image_stats_dict)
    
    # Save as CSV
    with open(os.path.join(root_directory,'image_stats.csv'), 'w', newline='') as csv_file:
        fieldnames = data_list[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data_list:
            writer.writerow(row)
            
    # Return the image statistics dictionary
    return image_stats_dict
    

def convert_stats_dict_to_list(image_stats_dict):
    # Initialize an empty list to store flattened data
    data_list = []

    # Extract all unique keys (headers) from the nested dictionary
    all_keys = set()
    for root_name, quad_data in image_stats_dict.items():
        for stats in quad_data.values():
            all_keys.update(stats.keys())

    # Convert the set of keys to a sorted list to ensure consistent order
    header = sorted(all_keys)

    # Iterate through the nested dictionary and flatten it
    for root_name, quad_data in image_stats_dict.items():
        for quad_val, stats in quad_data.items():
            # Create a dictionary for each row with all keys and default values
            row_data = {key: '' for key in header}
            row_data['root_name'] = root_name
            row_data['quad_val'] = quad_val
            row_data.update(stats)  # Update with actual statistics

            # Append the dictionary to the list
            data_list.append(row_data)
            
    return data_list


def parse_data_vs_quad(screen_name, image_stats_dict, stats_key):
    # Extract the data for the specified aline_name
    screen_data = image_stats_dict.get(screen_name, {})

    # Initialize lists to store the quad values and corresponding data values
    quad_values = []
    data_values = []

    # Loop through the quad values and data values for the specified aline_name
    for quad_val, stats in screen_data.items():
        quad_values.append(quad_val)
        data_values.append(stats.get(stats_key, None))

    # Pair quad values with data values and sort by quad values
    sorted_data = sorted(zip(quad_values, data_values), key=lambda x: x[0])

    # Unzip the sorted data to separate quad values and data values
    sorted_quad_values, sorted_data_values = zip(*sorted_data)
    
    # Return the sorted quad values and data values
    return sorted_quad_values, sorted_data_values
                


