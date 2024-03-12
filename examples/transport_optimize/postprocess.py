from shared import utils

def obj_f(J):
    
    utils.post_process_elegant_beamfiles()
    utils.make_beam_profile_images()
    utils.create_image_grid()
    
    utils.twiss_analysis()
    utils.sig_analysis()
    
    # Choose a filename
    filename = 'simulation_inputs.txt'

    # Write the dictionary to a file
    with open(filename, 'w') as f:
        for key, value in J['inputs'].items():
            f.write(f"{key}: {value}\n")
    
    
    return 0
