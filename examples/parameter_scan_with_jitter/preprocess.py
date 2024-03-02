import numpy as np
import yaml

# Path to your YAML file
file_path = 'preprocess_settings.yml'

# Step 1: Read the YAML file
with open(file_path, 'r') as file:
    preprocess_settings = yaml.safe_load(file)

def f_pre(J):
    # Example pre processing to modify the number of particles used
    particles = J['inputs']['bunched_beam.n_particles_per_bunch']
    # print(J['inputs'])

    momentum = J['inputs']['bunched_beam.Po']
    centroids = J['inputs']['bunched_beam.centroid']
    
    # Converting string to a list of floats
    cent_float_list = [float(i) for i in centroids.split(",")]

    # Converting list to a numpy array
    initial_centroids = np.array(cent_float_list)
    rnd = J['rand_stream'].random(2)

    # Set the seed
    np.random.seed(round(rnd[0]*100000000))

    position_jitter = 4E-6
    angle_jitter = 1.5E-3
    momentum_jitter = 10 #in units of gamma


    centroidx = np.random.normal(0, position_jitter)
    centroidxp = np.random.normal(0, angle_jitter)
    centroidy = np.random.normal(0, position_jitter)
    centroidyp = np.random.normal(0, angle_jitter)

    new_momentum = float(np.random.normal(0, momentum_jitter)*preprocess_settings['transverse_jitter']+momentum)

    centroids=np.array([centroidx,centroidxp,centroidy,centroidyp])*preprocess_settings['transverse_jitter']+initial_centroids

    # Convert the NumPy array to a single string
    centroid_str = ' '.join(centroids.astype(str))

    J['inputs']['bunched_beam.centroid'] = centroid_str
    J['inputs']['bunched_beam.Po'] = new_momentum

    print(J['inputs'])
    

    
    

    
    
    
    
