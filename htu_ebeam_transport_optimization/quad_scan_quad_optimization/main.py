""" Quad Scan Quad Optimization

The main program that optimizes quadrupole strength and placement by 
iteratively running a quadrupole scan to determine Twiss parameters, optimizing
magnet settings, and setting the quadrupoles with new values.

"""

from __future__ import annotations

from typing import Type, TYPE_CHECKING

from . import measure as measure_programs
from . import optimize as optimize_programs
from . import actuate as actuate_programs

if TYPE_CHECKING:
    from ..types import Measurement, OptimalParameters, QuadScanMeasurement, QuadConfiguration 

class DeviceParameterOptimizer:
    """ Program that iteratively adjusts device settings to optimize a target

    The optimization iterates through these programs:
        1. measure - quantify the state of the target now
        2. optimize - calculate optimal parameters to attain the desired target
        3. actuate - apply optimal parameters to devices
    
    """
    def __init__(self):
        pass

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
        'geecs_python_api': measure_programs.GEECSPythonAPITwissQuadScan,
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
                 twiss_parameter_measure_program: str | Type[measure_programs.QuadScanProgram] = 'manual',
                 quad_optimize_program: str | Type[optimize_programs.QuadOptimizeProgram] = 'elegant',
                 quad_set_program: str | Type[actuate_programs.QuadSetProgram] = 'manual',
                ): 
        """
        Parameters
        ----------
        twiss_parameter_measure_program : str or QuadScanProgram subclass
            A program - or name of one of the programs in MEASURE_PROGRAMS - 
            implementing a measure_twiss_parameters() method that returns the 
            Twiss parameters at screen ALine 3
        quad_optimize_program : str or QuadOptimizeProgram subclass
            A program - or name of one of the programs in OPTIMIZE_PROGRAMS - 
            that calculates the optimal new quadrupole parameters in order to 
            obtain matching at the undulator entrance.
        quad_set_program : str or QuadSetProgram subclass
            A program - or name of one of the programs in ACTUATE_PROGRAMS - 
            that applies the given parameters to the quadrupoles.
            
        """

        if isinstance(twiss_parameter_measure_program, str):
            twiss_parameter_measure_program = self.MEASURE_PROGRAMS[twiss_parameter_measure_program]
        if isinstance(quad_optimize_program, str):
            quad_optimize_program = self.OPTIMIZE_PROGRAMS[quad_optimize_program]
        if isinstance(quad_set_program, str):
            quad_set_program = self.ACTUATE_PROGRAMS[quad_set_program]

        self.quad_scan_program: measure_programs.QuadScanProgram = twiss_parameter_measure_program()
        self.quad_optimize_program: optimize_programs.QuadOptimizeProgram = quad_optimize_program()
        self.quad_set_program: actuate_programs.QuadSetProgram = quad_set_program()

    def measure(self) -> QuadScanMeasurement:
        return self.quad_scan_program.measure()

    def optimize(self, measurement: QuadScanMeasurement) -> QuadConfiguration:
        return self.quad_optimize_program.run_optimization(measurement)

    def actuate(self, optimal_quad_parameters: QuadConfiguration):
        self.quad_set_program.set_quad_properties(optimal_quad_parameters)
        # TODO: also need to keep track of optimal_quad_parameters to modify 
        # lattice file

    def stop_criteria(self) -> bool:
        # TODO
        return True

if __name__ == "__main__":
    qo = QuadrupoleOptimizer()
    qo.run()
