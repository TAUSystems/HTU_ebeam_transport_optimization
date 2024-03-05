import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
from shared import utils
from shared import quad_scan_analysis

import sys

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
                
def move_aux_files_to_jitter_sim(root_dir, final_dir_path):
    """
    Moves all auxiliary files from root_dir to final_dir_path.
    """
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isfile(item_path):  # Check if it's a file
            try:
                shutil.move(item_path, final_dir_path)
                print(f"Moved auxiliary file {item} to {final_dir_path}")
            except Exception as e:
                print(f"Error moving file {item}: {e}")
                
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
#
if __name__ == "__main__":
    if len(sys.argv) > 1:
        setting_value = sys.argv[1]
        print(f"Processing summary for setting value: {setting_value}")

        # Root directory path
        root_dir = 'elegant_scan'
        # Convert root_dir to an absolute path
        abs_root_dir = os.path.abspath(root_dir)

        # Final directory name based on the setting value
        final_dir_name = 'jitter_sim_' + setting_value
        # Final directory path
        final_dir_path = os.path.join(abs_root_dir, final_dir_name)

        # Now you can call your functions with setting_value being used
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
        cleanup_final_directory(final_dir_path)
        
        # Now, move auxiliary files from elegant_scan to jitter_sim_setting_value
        move_aux_files_to_jitter_sim(abs_root_dir, final_dir_path)
        
        # Determine the parent directory of root_dir to move the jitter_sim directory up one level
        parent_dir = os.path.dirname(abs_root_dir)
        target_final_dir_path = os.path.join(parent_dir, final_dir_name)

        # Attempt to move the jitter_sim_setting_value directory up one level
        try:
            shutil.move(final_dir_path, parent_dir)
            print(f"Successfully moved {final_dir_name} to {parent_dir}")
        except Exception as e:
            print(f"Error moving {final_dir_name} to {parent_dir}: {e}")

        # Finally, delete the original root_dir (elegant_scan) if it's now empty
        try:
            if os.listdir(abs_root_dir):  # Check if the directory is not empty
                print(f"{abs_root_dir} is not empty. Please check its contents before deletion.")
            else:
                shutil.rmtree(abs_root_dir)
                print(f"Deleted original directory: {abs_root_dir}")
        except Exception as e:
            print(f"Error deleting original directory {abs_root_dir}: {e}")


