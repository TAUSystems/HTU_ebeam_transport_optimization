"""
Module to host functions related to translating one file format to another.  Copying over Sam's code to translate w1
sdds binary files into a numpy array for reference, maybe someday entirely shift them from utils

-Chris
"""

import subprocess
import numpy as np
import glob
import struct
import os

const_lightspeed = 299792458  # m/s
const_electronmass = 0.511e6  # eV


def convert_npy_to_sdds(folder, npy_filename):
    # Read the numpy file
    rootname = os.path.splitext(npy_filename)[0]
    numpy_data = np.load(folder + rootname + ".npy")

    # Get into the appropriate units with appropriate ordering
    beam_x = numpy_data[0]
    beam_xp = numpy_data[1]
    beam_y = numpy_data[2]
    beam_yp = numpy_data[3]
    beam_t = numpy_data[4] / const_lightspeed
    beam_p = numpy_data[5] / const_electronmass

    # Convert to csv and write
    csv_data = np.column_stack([beam_x, beam_xp, beam_y, beam_yp, beam_t, beam_p])
    header = ",".join(['x', 'xp', 'y', 'yp', 't', 'p'])  # Define the column names for the CSV
    csv_filename = folder + rootname + ".csv"
    np.savetxt(csv_filename, csv_data, delimiter=",", header=header, comments="")

    # Convert csv to sdds using the command line
    sdds_filename = folder + rootname + ".sdds"
    subprocess.run(['csv2sdds', csv_filename, '-columnData=name=x,type=double', '-columnData=name=xp,type=double',
                    '-columnData=name=y,type=double', '-columnData=name=yp,type=double',
                    '-columnData=name=t,type=double', '-columnData=name=p,type=double', sdds_filename])

    return sdds_filename


def post_process_elegant_beamfiles():
    # Loop through all files with the .w1 extension and execute the command
    for filename in glob.glob('*.w1'):
        subprocess.run(
            ['sddsprocess', filename, f'{filename}.proc', '-define=parameter,speedOfLight,2.999792458e8,units=m',
             '-define=parameter,speedOfLightS,1.0e0,units=s',
             '-define=column,positionZ,"t s speedOfLight speedOfLightS / / pCentral sqr 1 + sqrt * pCentral / -",units=m'])

    # Loop through all files with the .proc extension
    for filename in glob.glob('*.proc'):
        subprocess.run(['sdds2plaindata', filename, f'{filename}.plainbin', '-outputMode=binary',
                        '-parameter=s', '-parameter=Charge',
                        '-column=x', '-column=xp', '-column=y', '-column=yp',
                        '-column=t', '-column=p', '-column=dt', '-column=positionZ'])


def read_plainbin_beamfile(file_name):
    num_cols = 8
    # Open the binary file for reading
    with open(file_name, 'rb') as f:
        # Read header
        header = struct.unpack('i', f.read(4))[0]  # Integer32
        real1 = struct.unpack('d', f.read(8))[0]  # Real64
        real2 = struct.unpack('d', f.read(8))[0]  # Real64
        head = (header, real1, real2)

        # Read beam_phase
        beam_phase = [struct.unpack('d', f.read(8))[0] for _ in range(head[0] * num_cols)]

        # Reshape beam_phase to a 2D list
        beam_phase = [beam_phase[i:i + num_cols] for i in range(0, len(beam_phase), num_cols)]

        # Adjust the last column
        # mean_val = sum(row[7] for row in beam_phase) / len(beam_phase)
        # for row in beam_phase:
        #     row[7] = (row[7] - mean_val) * 2.998e8

    beam_phase = np.array(beam_phase)

    return beam_phase
