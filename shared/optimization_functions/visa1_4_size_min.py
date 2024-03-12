import os
import numpy as np
import imageio.v2 as imageio

# Function to generate a 2D Gaussian mask
def generate_2d_gaussian_mask(shape, mask_dict):
    sigma_x = mask_dict['sigma_x']
    sigma_y = mask_dict['sigma_y']
    dx = mask_dict['dx']
    dy = mask_dict['dy']

    m, n = shape
    y, x = np.ogrid[-m//2:m//2, -n//2:n//2]
    # y += dy
    # x += dx
    print(shape)
    h = np.exp(-((x - dx)**2 + (x - dy)**2) / (2 * sigma_x * sigma_y))
    h[h < np.finfo(h.dtype).eps * h.max()] = 0
    return h

def cost_function(image_path,mask_dict):
    
    image = imageio.imread(image_path)
    # Generate the Gaussian mask
    gaussian_mask = generate_2d_gaussian_mask(image.shape, mask_dict)
    # Multiply the image by the Gaussian mask
    gaussian_image = image.astype(np.float32) * gaussian_mask
    # Sum the values in the image
    image_sum = gaussian_image.sum()
    
    return image_sum
    

def obj_f(sim_directory):
    """
    Calculate the objective function value for simulation results in a specified directory.

    Parameters:
    - sim_directory: The directory where simulation images are stored.

    Returns:
    - The negative square root of the sum of squares of the cost function values for each image.
    """
    
    print('sim_directory: ', sim_directory)
    mask_dict = {'sigma_x': 20, 'sigma_y': 20, 'dx': 0, 'dy': 0}
    
    # List of image file names
    image_files = ["VisaEBeam1_raw.png", "VisaEBeam2_raw.png", "VisaEBeam3_raw.png", "VisaEBeam4_raw.png"]
    
    # Initialize the sum of squares
    sum_of_squares = 0
    
    # Loop through each image file, calculate its cost, and add to the sum of squares
    for image_file in image_files:
        image_path = os.path.join(sim_directory, image_file)
        cost = cost_function(image_path, mask_dict)  # Assuming cost_function can take the full path
        sum_of_squares += cost**2
    
    # Calculate the objective value
    obj = -np.sqrt(sum_of_squares)
    
    print(obj)
    
    return obj
    

    
    

    
    
    
    
