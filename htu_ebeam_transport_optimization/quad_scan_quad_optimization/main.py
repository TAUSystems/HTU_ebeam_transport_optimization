""" Quad Scan Quad Optimization

The main program that optimizes quadrupole strength and placement by 
iteratively running a quadrupole scan to determine Twiss parameters, optimizing
magnet settings, and setting the quadrupoles with new values.

"""

from __future__ import annotations

from ..types import Measurement, OptimalParameters
from ..types import TwissParameters
from ..types import QuadScanImage, QuadConfiguration

from . import measure as measure_programs
from . import optimize as optimize_programs
from . import actuate as actuate_programs

class DeviceParameterOptimizer:
    """ Program that iteratively adjusts device settings to optimize a target

    The optimization iterates through these programs:
        1. measure - quantify the state of the target now
        2. optimize - calculate optimal parameters to attain the desired target
        3. actuate - apply optimal parameters to devices
    
    """

    def measure(self) -> Measurement:
        """ A program that quantifies the current state of the optimization target
        """
        raise NotImplementedError("Derived class should implement measure()")
    
    def optimize(self, measurement: Measurement) -> OptimalParameters:
        """ A program that calculates optimal device parameters
        """
        raise NotImplementedError("Derived class should implement optimize()")
    
    def actuate(self, optimal_parameters: OptimalParameters) -> None:
        """ A program that applies optimal parameters to devices
        """
        raise NotImplementedError("Derived class should implement actuate()")

    def stop_criteria(self) -> bool:
        raise NotImplementedError("Derived class should implement stop_criteria()")

    def run_one_iteration(self):
        measurement: Measurement = self.measure()
        optimal_parameters: OptimalParameters = self.optimize(measurement)
        self.actuate(optimal_parameters)

    def run(self):
        while not self.stop_criteria():
            self.run_one_iteration()


class QuadrupoleOptimizer(DeviceParameterOptimizer):
    """ Optimizes quadrupole settings to get e-beam matching at undulator entrance
        
    """

    MEASURE_PROGRAMS = {
        'manual': measure_programs.ManualQuadScan,
        'geecs_python_api': measure_programs.GEECSPythonAPIQuadScan,
    }

    OPTIMIZE_PROGRAMS = {
        'elegant': optimize_programs.ElegantOptimizer,
        'rsopt': optimize_programs.RSOptOptimizer,
        'phase_space_reconstruction': optimize_programs.PhaseSpaceReconstructionOptimizer,
    }

    ACTUATE_PROGRAMS = {
        'manual': actuate_programs.ManualQuadSet,
        'geecs_python_api': actuate_programs.GEECSPythonAPIQuadSet,
    }

    def __init__(self, 
                 quad_scan_method: str = 'manual',
                 quad_optimize_method: str = 'elegant',
                 quad_set_method: str = 'manual',
                ): 
        """
        Parameters
        ----------
        quad_scan_method : str, optional
            _description_, by default 'manual'
        quad_optimize_method : str, optional
            _description_, by default 'elegant'
        quad_set_method : str, optional
            _description_, by default 'manual'
        """

        self.quad_scan_program: measure_programs.QuadScanProgram = self.MEASURE_PROGRAMS[quad_scan_method]()
        self.quad_optimize_program: optimize_programs.QuadOptimizeProgram = self.OPTIMIZE_PROGRAMS[quad_optimize_method]()
        self.quad_set_program: actuate_programs.QuadSetProgram = self.ACTUATE_PROGRAMS[quad_set_method]()


    def measure(self):
        twiss_parameters: TwissParameters = self.quad_scan_program.run_quad_scan()
        return twiss_parameters
    
    def optimize(self, twiss_parameters: TwissParameters):
        optimal_quad_configuration: QuadConfiguration = self.quad_optimize_program.run_optimization(twiss_parameters)
        return optimal_quad_configuration

    def actuate(self, optimal_quad_parameters: QuadConfiguration):
        self.quad_set_program.set_quad_properties(optimal_quad_parameters)

if __name__ == "__main__":
    qo = QuadrupoleOptimizer()
    qo.run()
