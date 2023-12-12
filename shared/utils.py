import subprocess
import numpy as np
import sys
import os
import glob
import struct
import matplotlib.pyplot as plt
from pathlib import Path  # Importing Path
from PIL import Image
from collections import OrderedDict
import imageio

from rsbeams.rsplot import util
from rsbeams.rsdata.SDDS import readSDDS
# from rsbeams.rsplot import beam_plots

#dict for screens, their sizes, and resolution
screens_dict = OrderedDict({'TCPhosphor':[.01,.000037],"ChicaneSlit":[.01,.00003378],"DCPhosphor":[0.01,.0000168],
                'Phosphor1':[.01,.0000165],"Aline1":[.01,.00002217],"Aline2":[0.01,.00002394],
                'Aline3':[.01,.0000244],"VisaEBeam1":[.0015,.00000755],"VisaEBeam2":[0.0015,.00000755],
                'VisaEBeam3':[.0015,.00000752],"VisaEBeam4":[.0015,.00000741],"VisaEBeam5":[0.0015,.00000768],
                'VisaEBeam6':[.0015,.00000763],"VisaEBeam7":[.0015,.00000735],"VisaEBeam8":[0.0015,.00000707]
                })
                
def twiss_analysis():
    # Get the current working directory
    current_directory = os.getcwd()

    # Find the .twi file in the current directory
    twi_files = glob.glob(str(Path(current_directory) / '*.twi'))

    if not twi_files:
        raise FileNotFoundError("No .twi file found in the specified directory.")

    # Use the first .twi file found
    twi_file_path = twi_files[0]

    save_path = os.path.join(os.getcwd(), twi_file_path + '.png')

    # Read Twiss file
    twiss_file = readSDDS(Path(twi_file_path))
    twiss_file.read()

    plt.figure()

    twiss_columns = twiss_file.columns.squeeze()

    plt.plot(twiss_columns['s'], twiss_columns['betax'], label=r'$\beta_x$')
    plt.plot(twiss_columns['s'], twiss_columns['betay'], label=r'$\beta_y$')
    plt.legend()
    plt.xlabel('s (meters)')
    plt.ylabel('Beta function ($m$)')

    # Save the plot
    plt.savefig(save_path)

    # Close the plot to free up memory
    plt.close()
    



def beamline_profile(sdds, page=0, quantities=None, xlim=None, ylim=None, save=None, show=False):
    """ Plot quantities vs position. Adapted from rsplot

    Args:
        sdds: Open SDDS file from rsbeams.rsdata.readSDDS
        page: [0] Page number in SDDS file to plot from.
        quantities: (list) List of quantities to place on plot.
        xlim: (tuple) (min, max) Manually set plot range in x.
        ylim: (tuple) (min, max) Manually set plot range in y.
        save: (str) Path to file (with extension) to save plot.
    """
    sdds_columns = sdds.columns[page]

    if not quantities:
        quantities = ['Sx', 'Sy']

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 6),
                                   sharex=True,
                                   gridspec_kw={'height_ratios': [1, 8]})

    ax1.axis('off')
    util.plot_profile(sdds_columns, ax1, height=0.25)
    for quant in quantities:
        ax2.plot(sdds_columns['s'], sdds_columns[quant], label=util.format_symbol(sdds.column_symbol(quant)) if sdds.column_symbol(quant) != '' else sdds.column_description(quant))

    ax2.legend(fontsize=16)
    ax2.set_xlabel('s (m)', fontsize=16)

    ylabel = ','.join([util.format_symbol(sdds.column_symbol(quant)) if sdds.column_symbol(quant) != '' else sdds.column_description(quant) for quant in quantities])
    ylabel += ' (' + ','.join([util.format_symbol(sdds.column_units(quant)) if sdds.column_units(quant) != '' else '$-$' for quant in quantities]) + ')'
    ax2.set_ylabel(ylabel, fontsize=16)
    if xlim:
        ax2.set_xlim(*xlim)
    if ylim:
        ax2.set_ylim(*ylim)
    if save:
        plt.savefig(save)
    if show:
        plt.show()
    
def sig_analysis():   
    # Get the current working directory
    current_directory = os.getcwd()

    # Find the .sig file in the current directory
    sig_files = glob.glob(str(Path(current_directory) / '*.sig'))

    if not sig_files:
        raise FileNotFoundError("No .sig file found in the specified directory.")

    # Use the first .sig file found
    sig_file_path = sig_files[0]

    save_path = os.path.join(os.getcwd(), sig_file_path + '.png')

    # Read sigma file
    sigma_file = readSDDS(Path(sig_file_path))
    sigma_file.read()
    
    beamline_profile(sigma_file, quantities=['Sx', 'Sy',],save=save_path)
    
    return     


def post_process_elegant_beamfiles():
    # Loop through all files with the .w1 extension and execute the command
    for filename in glob.glob('*.w1'):
        subprocess.run(['sddsprocess', filename, f'{filename}.proc', '-define=parameter,speedOfLight,2.999792458e8,units=m', 
                        '-define=parameter,speedOfLightS,1.0e0,units=s', 
                        '-define=column,positionZ,"t s speedOfLight speedOfLightS / / pCentral sqr 1 + sqrt * pCentral / -",units=m'])

    # Loop through all files with the .proc extension
    for filename in glob.glob('*.proc'):
        subprocess.run(['sdds2plaindata', filename, f'{filename}.plainbin', '-outputMode=binary', 
                        '-parameter=s', '-parameter=Charge', 
                        '-column=x', '-column=xp', '-column=y', '-column=yp', 
                        '-column=t', '-column=p', '-column=dt', '-column=positionZ'])
 
def read_plainbin_beamfile(file_name):
    numCols = 8
    # Open the binary file for reading
    with open(file_name, 'rb') as f:
        # Read header
        header = struct.unpack('i', f.read(4))[0]  # Integer32
        real1 = struct.unpack('d', f.read(8))[0]  # Real64
        real2 = struct.unpack('d', f.read(8))[0]  # Real64
        head = (header, real1, real2)

        # Read beamPhase
        beamPhase = [struct.unpack('d', f.read(8))[0] for _ in range(head[0] * numCols)]

        # Reshape beamPhase to a 2D list
        beamPhase = [beamPhase[i:i+numCols] for i in range(0, len(beamPhase), numCols)]

        # Adjust the last column
        mean_val = sum(row[7] for row in beamPhase) / len(beamPhase)
        for row in beamPhase:
            row[7] = (row[7] - mean_val) * 2.998e8

    beamPhase=np.array(beamPhase)
    
    return beamPhase
    
def beam_profile(x_data, y_data, screen, root_dir='local'):

    size, resolution = screens_dict[screen]

    # Create a mask for filtering data points
    mask = (np.abs(x_data) < size) & (np.abs(y_data) < size)

    # Use the mask to select data points
    filtered_data = np.column_stack((x_data[mask], y_data[mask]))
    
    # Create the histogram
    hist, x_edges, y_edges = np.histogram2d(
        filtered_data[:, 0], filtered_data[:, 1],
        bins=[np.arange(-size, size + resolution, resolution),
              np.arange(-size, size + resolution, resolution)]
    )
    
    hist_16bit = hist.astype(np.uint16)
    # save_path_hist = os.path.join(os.getcwd(), screen + '_raw.png')
    if root_dir=='local':
        save_path_hist = os.path.join(os.getcwd(), screen + '_raw.png')
        save_path = os.path.join(os.getcwd(), screen + '.png')
    else:
        save_path_hist = os.path.join(root_dir, screen + '_raw.png')
        save_path = os.path.join(root_dir, screen + '.png')
    
    # print('save_path',save_path)
    # Save the histogram as a 16-bit grayscale image (PNG)
    imageio.imwrite(save_path_hist, hist_16bit)
    
    # Convert edges to millimeters
    x_edges_mm = x_edges * 1000
    y_edges_mm = y_edges * 1000
    size = size * 1000

    # Create the extent for plotting in mm
    extent_mm = [x_edges_mm[0], x_edges_mm[-1], y_edges_mm[0], y_edges_mm[-1]]

    # Plot the 2D histogram as an array plot
    plt.imshow(hist.T, extent=extent_mm, origin='lower', aspect='equal', cmap='viridis')

    # Set axis labels and title
    plt.xlabel('X (mm)')
    plt.ylabel('Y (mm)')
    plt.title(screen)

    # Set axis limits to plus/minus 0.01
    plt.xlim(-size, size)
    plt.ylim(-size, size)

    plt.savefig(save_path)

    # Clear the current figure to free up memory
    plt.close()
    
def beam_profile_from_plainbin_file(file_name, root_dir='local'):
    beam_phase = read_plainbin_beamfile(file_name)  # Consider replacing with file_name
    parts = file_name.split('.')
    x_data = beam_phase[:, 0]
    y_data = beam_phase[:, 2]
    screen_name = parts[0]
    beam_profile(x_data, y_data, screen_name, root_dir)
    
def beam_profile_from_np_array(phase_space, screen_name,root_dir='local'):
    x_data = phase_space[:, 0]
    y_data = phase_space[:, 2]
    beam_profile(x_data, y_data, screen_name, root_dir)
    
def make_beam_profile_images():
    # Looping over the keys in screens_dict
    for screen_name in screens_dict.keys():
        # Construct the file name for each screen. Assuming the file format you need.
        file_name = screen_name + '.w1.proc.plainbin'

        # Call the beam_profile function for each screen
        beam_profile_from_plainbin_file(file_name)
        
def make_beam_profile_images_jitter(combined_phase_dict,root_dir='local'):
    # Looping over the keys in screens_dict
    for screen_name in screens_dict.keys():
        beam_profile_from_np_array(combined_phase_dict[screen_name],screen_name,root_dir)
        

def auto_crop_image(image):
    """
    Automatically crops the image to remove excess white space.
    Args:
    - image (PIL.Image): Image to be cropped.

    Returns:
    - PIL.Image: Cropped image.
    """
    grayscale = image.convert('L')
    grayscale_np = np.array(grayscale)
    binary = grayscale_np < 254  # Adjust the threshold value as needed
    non_zero_coords = np.argwhere(binary)
    
    if len(non_zero_coords) > 0:
        min_y, min_x = non_zero_coords.min(axis=0)
        max_y, max_x = non_zero_coords.max(axis=0)
        bbox = (min_x-4, min_y-4, max_x+4, max_y+4)
        return image.crop(bbox)
    return image

def create_image_grid(root_dir='local'):
    
    # Define the correct order of the images
    correct_order = screens_dict.keys()

    # Append the file extension to the image names
    ordered_images = [f"{name}.png" for name in correct_order]

    # Path to the folder containing the images
    if root_dir=='local':
        folder_path = os.getcwd()  # Or specify your folder path
    else:
        folder_path = root_dir  # Or specify your folder path
    
    # print('grid image path: ',folder_path)
    # Create a grid for displaying the images
    fig, axes = plt.subplots(3, 5, figsize=(25, 15))  # Adjust the size as needed
    axes = axes.ravel()

    # Adjust subplot parameters to reduce spacing
    plt.subplots_adjust(left=1.99, right=2, top=0.1, bottom=0.09, wspace=1, hspace=5)
    
    # Load, crop, and display each image in the grid
    for ax, img_name in zip(axes.ravel(), ordered_images):
        img_path = os.path.join(folder_path, img_name)
        # print('grid image image path: ',img_path)
        with Image.open(img_path) as img:
            cropped_img = auto_crop_image(img)
            ax.imshow(cropped_img)
            ax.axis('off')  # Hide the axes
    # Save the figure before showing
    plt.tight_layout()
    plt.savefig(os.path.join(folder_path, 'graphics_grid.png'), bbox_inches='tight')
    plt.close()
    
def collect_watchpoint_file_paths(root_dir, file_names, extension):
    """
    Collects paths of specific files within a directory structure.

    Args:
    root_dir (str): The root directory to start the search.
    file_names (list): List of file names to search for.

    Returns:
    dict: A dictionary where each key is a file name and the value is a list of paths to that file.
    """
    file_paths = {name: [] for name in file_names}
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            for name in file_names:
                if file.startswith(name) and file.endswith(extension):
                    full_path = os.path.join(dirpath, file)
                    file_paths[name].append(full_path)
    return file_paths
    
def collect_elegant_output_file_paths(root_dir, extension):
    """
    Collects paths of specific files within a directory structure that have the given extension

    Args:
    root_dir (str): The root directory to start the search.
    extension: the file extension being sought out

    Returns:
    dict: A dictionary where each key is a file name and the value is a path to that file.
    """
    file_paths = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(extension):
                parent_directory = os.path.basename(dirpath)
                full_path = os.path.join(dirpath, file)
                file_paths[parent_directory] = full_path
    return file_paths
    
# Function to read specific values from the file and store them in a dictionary
def read_sim_input_keys_values(file_path, keys):
    # Dictionary to store the required values
    required_values = {}

    # Open and read the file
    with open(file_path, 'r') as file:
        for line in file:
            # Iterate through each specified key
            for key in keys:
                # Check if the line contains the current key
                if key in line:
                    key_from_file, value = line.split(":")
                    required_values[key_from_file.strip()] = float(value.strip())
                    break  # Break the loop once the key is found

    return required_values
    
def read_sim_input_file(file_path):
    # Initialize an empty dictionary to store the data
    input_data = {}

    # Open the file for reading
    with open(file_path, "r") as file:
        for line in file:
            # Split each line into key and value using ':' as the separator
            parts = line.strip().split(':')
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                input_data[key] = value
    return input_data

    
def collect_elegant_output_file_paths_with_sim_input_keys(root_dir, extension, keys):
    """
    Collects paths of specific files within a directory structure that have the given extension

    Args:
    root_dir (str): The root directory to start the search.
    extension: the file extension being sought out

    Returns:
    dict: A dictionary where each key is a file name and the value is a path to that file.
    """
    file_paths = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(extension):
                parent_directory = os.path.basename(dirpath)
                sim_inputs = read_sim_input_keys_values(os.path.join(dirpath, "simulation_inputs.txt"),keys)
                full_path = os.path.join(dirpath, file)
                file_paths[parent_directory] = {'path':full_path, 'sim_inputs':sim_inputs}
    return file_paths
    
def create_sim_dict(root_dir, extension):
    """
    Collects paths of specific files within a directory structure that have the given extension

    Args:
    root_dir (str): The root directory to start the search.
    extension: the file extension being sought out

    Returns:
    dict: A dictionary where each key is a file name and the value is a path to that file.
    """
    file_paths = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(extension):
                parent_directory = os.path.basename(dirpath)
                sim_inputs = read_sim_input_file(os.path.join(dirpath,"simulation_inputs.txt"))
                full_path = os.path.join(dirpath, file)
                file_paths[parent_directory] = {'path':full_path, 'sim_inputs':sim_inputs}
    return file_paths
    
    
def process_centroid_files(path_dict):
    """
    Processes files specified in the path dictionary.

    Args:
    path_dict (dict): Dictionary with file paths.

    Returns:
    dict: A dictionary with processed data for each file.
    """
    processed_data = {}

    for parent_dir, file_path in path_dict.items():
        # Read the file
        file_data = readSDDS(file_path)
        file_data.read()

        # Extract the data
        columns = file_data.columns.squeeze()
        x_data = columns['s']
        y_data = columns['Cx']

        # Store the processed data in a dictionary
        processed_data[parent_dir] = {'x': x_data, 'y': y_data}

    return processed_data
    
def get_Cx_Cy_s(cen_file_path):
    """
    Processes files specified in the path dictionary.

    Args:
    path_dict (dict): Dictionary with file paths.

    Returns:
    dict: A dictionary with processed data for each file.
    """
    
    file_data = readSDDS(cen_file_path)
    file_data.read()
    # Extract the data
    columns = file_data.columns.squeeze()
    s_data = columns['s']
    cx_data = columns['Cx']
    cy_data = columns['Cy']

    return {'Cx': cx_data, 'Cy': cy_data,'s':s_data}
    
def get_mon_kicker_locations(cen_file_path):
    """
    Processes files specified in the path dictionary.

    Args:
    path_dict (dict): Dictionary with file paths.

    Returns:
    dict: A dictionary with processed data for each file.
    """
    
    file_data = readSDDS(cen_file_path)
    file_data.read()
    # Extract the data
    columns = file_data.columns.squeeze()
    element_data = columns['ElementNames']
    cx_data = columns['Cx']
    cy_data = columns['Cy']

    return {'Cx': cx_data, 'Cy': cy_data,'s':s_data}
    
def compute_centroid_stats(processed_data_dict):
    # Assuming all x_data are the same across datasets
    x_data = list(processed_data_dict.values())[0]['x']

    # Aggregate all y_data
    all_y_data = [data['y'] for data in processed_data_dict.values()]

    # Compute average and standard deviation
    avg_y = np.mean(all_y_data, axis=0)
    std_dev_y = np.std(all_y_data, axis=0)

    return x_data, avg_y, std_dev_y

def plot_centroid_jitter_data(x_data, avg_y, std_dev_y):
    plt.figure(figsize=(10, 6))
    plt.errorbar(x_data, avg_y, yerr=std_dev_y, fmt='-', ecolor='lightgray', elinewidth=3, capsize=0)
    plt.xlabel('s (m)')
    plt.ylabel('Average centroid and std')
    plt.grid(True)
    plt.show()

def concatenate_beamfiles(file_paths):
    """
    Concatenates multiple beam files into a single NumPy array.

    Args:
    file_paths (list): List of paths to the beam files.

    Returns:
    numpy.ndarray: A single NumPy array containing all the data.
    """
    all_data = []
    for file_path in file_paths:
        data = read_plainbin_beamfile(file_path)
        all_data.append(data)

    return np.vstack(all_data)
    
def combine_phase_files(root_directory):
    # List of file names to search for
    file_names = screens_dict.keys()
    
    # Root directory of your file structure
    # root_directory = 'elegant_scan'  # Replace with the path to your root directory

    # Collect file paths
    collected_paths = collect_watchpoint_file_paths(root_directory, file_names,'plainbin')
    # print(collected_paths)

    # Iterate through each key in the dictionary and process the files
    combined_data_dict = {}
    for key, file_paths in collected_paths.items():
        if file_paths:  # Check if there are files for this key
            combined_data_dict[key] = concatenate_beamfiles(file_paths)
            # print(f"Processed {len(file_paths)} files for key '{key}'.")
        else:
            print(f"No files found for key '{key}'.")
            
    return combined_data_dict
