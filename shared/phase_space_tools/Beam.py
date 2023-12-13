"""
Quick classes to store an electron beam's 6D phase space
"""

import numpy as np


def calculate_geometric_emittance(x, xp):
    dx = x - np.average(x)
    dxp = xp - np.average(xp)
    sigma_x2 = np.average(np.square(dx))
    sigma_xp2 = np.average(np.square(dxp))
    sigma_xxp = np.average(dx * dxp)
    return np.sqrt(sigma_x2 * sigma_xp2 - np.square(sigma_xxp))


class Beam:
    """
    The coordinates are defined as follows:
    x, y, z: [m]
    px, py:  [rad]
    pz:      [eV]
    """

    def __init__(self, n_particles):
        self.n_particles = n_particles
        self.x = np.zeros(n_particles)
        self.px = np.zeros(n_particles)
        self.y = np.zeros(n_particles)
        self.py = np.zeros(n_particles)
        self.z = np.zeros(n_particles)
        self.pz = np.zeros(n_particles)

    def set_phase_space(self, x, px, y, py, z, pz):
        self.set_x(x)
        self.set_px(px)
        self.set_y(y)
        self.set_py(py)
        self.set_z(z)
        self.set_pz(pz)

    def calculate_x_emittance_n(self):
        emit_x = calculate_geometric_emittance(self.x, self.px)
        return emit_x * self.calculate_gamma_lorentz()

    def calculate_y_emittance_n(self):
        emit_y = calculate_geometric_emittance(self.y, self.py)
        return emit_y * self.calculate_gamma_lorentz()

    def calculate_gamma_lorentz(self):
        electron_rest_mass = 0.511e6  # eV
        beam_gamma = self.pz/electron_rest_mass
        return np.average(beam_gamma)

    def calculate_average_energy_eV(self):
        return np.average(self.pz)

    def calculate_energy_spread(self):
        average_energy = self.calculate_average_energy_eV()
        return np.sqrt(np.average(np.square(self.pz - average_energy)))/average_energy * 100

    def calculate_x_average(self):
        return np.average(self.x)

    def calculate_y_average(self):
        return np.average(self.y)

    def calculate_px_average(self):
        return np.average(self.px)

    def calculate_py_average(self):
        return np.average(self.py)

    def calculate_x_beta(self):
        sigma_x2 = np.average(np.square(self.x - self.calculate_x_average()))
        return sigma_x2/calculate_geometric_emittance(self.x, self.px)

    def calculate_y_beta(self):
        sigma_y2 = np.average(np.square(self.y - self.calculate_y_average()))
        return sigma_y2/calculate_geometric_emittance(self.y, self.py)

    def calculate_x_gamma(self):
        sigma_xp2 = np.average(np.square(self.px - self.calculate_px_average()))
        return sigma_xp2 / calculate_geometric_emittance(self.x, self.px)

    def calculate_y_gamma(self):
        sigma_yp2 = np.average(np.square(self.py - self.calculate_py_average()))
        return sigma_yp2 / calculate_geometric_emittance(self.y, self.py)

    def calculate_x_alpha(self):
        dx = self.x - self.calculate_x_average()
        dxp = self.px - self.calculate_px_average()
        sigma_xxp = -np.average(dx * dxp)
        return sigma_xxp / calculate_geometric_emittance(self.x, self.px)

    def calculate_y_alpha(self):
        dy = self.y - self.calculate_y_average()
        dyp = self.py - self.calculate_py_average()
        sigma_yyp = -np.average(dy * dyp)
        return sigma_yyp / calculate_geometric_emittance(self.y, self.py)

    def set_x(self, x):
        self.x = np.copy(x)

    def set_px(self, px):
        self.px = np.copy(px)

    def set_y(self, y):
        self.y = np.copy(y)

    def set_py(self, py):
        self.py = np.copy(py)

    def set_z(self, z):
        self.z = np.copy(z)

    def set_pz(self, pz):
        self.pz = np.copy(pz)

    def get_n_particles(self):
        return self.n_particles

    def get_x(self):
        return self.x

    def get_px(self):
        return self.px

    def get_y(self):
        return self.y

    def get_py(self):
        return self.py

    def get_z(self):
        return self.z

    def get_pz(self):
        return self.pz


class NumpyBeam(Beam):

    def __init__(self, filename, adjust_to_average_energy_MeV=None, is_alternate_ordering=False):
        """
        Initialize a beam using a 6D phase space saved in a .npy file
        :param filename: Filename to .npy file with 6D beam distribution, by default we are assuming that the file is
                         saved as x,px,y,py,z,pz with pz saved as eV, but some older version are saved otherwise
        :param adjust_to_average_energy_MeV: Optional, legacy parameter to convert from fraction offset to eV
        :param is_alternate_ordering: Optional, legacy flag for older files saved as x,y,z,px,py,pz
        """
        beam_data = np.load(filename)
        super().__init__(np.shape(beam_data)[1])

        if adjust_to_average_energy_MeV is None:
            energy_eV = beam_data[5]
        else:
            energy_eV = (adjust_to_average_energy_MeV * (beam_data[5] + 1)) * 1e6
        if is_alternate_ordering:
            self.set_phase_space(beam_data[0], beam_data[3], beam_data[1], beam_data[4], beam_data[2], energy_eV)
        else:
            self.set_phase_space(beam_data[0], beam_data[1], beam_data[2], beam_data[3], beam_data[4], energy_eV)
