import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from shared import utils
from shared import quad_scan_analysis

def flatten_and_move_sim_dirs(root_dir, final_dir_name):
    """
    Flatten the directory structure by moving "simxxx" directories up to the root directory,
    then move these directories into a final directory named 'final_dir_name'.

    Parameters:
    root_dir (str): The root directory containing "worker" directories.
    final_dir_name (str): The name of the final directory to move "simxxx" directories into.
    """
    final_dir_path = os.path.join(root_dir, final_dir_name)
    
    # Create the final directory if it doesn't exist
    if not os.path.exists(final_dir_path):
        os.makedirs(final_dir_path)
    
    # List all items in the root directory
    for worker_dir in os.listdir(root_dir):
        worker_path = os.path.join(root_dir, worker_dir)
        
        # Proceed if the item is a directory (ignores files)
        if os.path.isdir(worker_path):
            for sim_dir in os.listdir(worker_path):
                sim_path = os.path.join(worker_path, sim_dir)
                
                # Ensure it is a directory to be moved
                if os.path.isdir(sim_path):
                    # Construct new path for the sim directory at the root level temporarily
                    new_sim_path = os.path.join(root_dir, sim_dir)
                    
                    # Move to root_dir first to avoid path issues
                    try:
                        shutil.move(sim_path, root_dir)
                    except Exception as e:
                        print(f"Error moving {sim_path} to {root_dir}: {e}")
            
            # Delete the worker directory
            try:
                shutil.rmtree(worker_path)
            except Exception as e:
                print(f"Error deleting {worker_path}: {e}")

    # Now move all simxxx directories from root_dir to final_dir_name
    for sim_dir in os.listdir(root_dir):
        sim_path = os.path.join(root_dir, sim_dir)
        
        # Check if it's a directory and not the final directory
        if os.path.isdir(sim_path) and sim_dir != final_dir_name:
            final_sim_path = os.path.join(final_dir_path, sim_dir)
            try:
                shutil.move(sim_path, final_sim_path)
            except Exception as e:
                print(f"Error moving {sim_path} to {final_sim_path}: {e}")
                
def postprocess(directory_path): 
     
    fpaths=utils.collect_elegant_output_file_paths(directory_path,'cen')
    print('print fpaths:',fpaths)
    combined_phase=utils.combine_phase_files(directory_path)
    utils.make_beam_profile_images_jitter(combined_phase,directory_path)

    utils.create_image_grid(directory_path)   
    
def cleanup_final_directory(final_dir_path):
    """
    Perform final cleanup in the final directory by deleting all processed 'simxxx' directories.

    Parameters:
    final_dir_path (str): The path to the final directory containing all 'simxxx' directories.
    """
    # List all items in the final directory
    for sim_dir in os.listdir(final_dir_path):
        sim_path = os.path.join(final_dir_path, sim_dir)
        
        # Proceed if the item is a directory
        if os.path.isdir(sim_path):
            try:
                shutil.rmtree(sim_path)
                print(f"Deleted directory: {sim_path}")
            except Exception as e:
                print(f"Error deleting {sim_path}: {e}")

# Example usage
root_dir = 'elegant_scan'  # Adjust this to your path
final_dir_name = 'jitter_sim'
flatten_and_move_sim_dirs(root_dir, final_dir_name)
                    
# Iterate over all entries in the root directory
for entry_name in os.listdir(root_dir):
    print('Entry name: ', entry_name)
    entry_path = os.path.join(root_dir, entry_name)

    # Check if the entry is a directory before proceeding
    if os.path.isdir(entry_path):
        postprocess(entry_path)
    else:
        print('Skipping, not a directory: ', entry_name)
        

# After all processing is done, call cleanup_final_directory
final_dir_path = os.path.join(root_dir, final_dir_name)
cleanup_final_directory(final_dir_path)

                            




