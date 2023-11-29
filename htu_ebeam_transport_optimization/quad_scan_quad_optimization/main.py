""" Quad Scan Quad Optimization

The main program that optimizes quadrupole strength and placement by 
iteratively running a quadrupole scan to determine Twiss parameters, optimizing
magnet settings, and setting the quadrupoles with new values.

"""

from __future__ import annotations

from ..types import QuadScanImage, QuadConfiguration

from . import scan as scan_programs
from . import optimize as optimize_programs
from . import set as set_programs

class QuadScanQuadOptimization:
    """ Program that iteratively runs the Quad optimization process
    """

    QUAD_SCAN_PROGRAMS = {
        'manual': scan_programs.ManualQuadScan,
        'geecs_python_api': scan_programs.GEECSPythonAPIQuadScan,
    }

    QUAD_OPTIMIZE_PROGRAMS = {
        'elegant': optimize_programs.ElegantOptimizer,
        'rsopt': optimize_programs.RSOptOptimizer,
        'phase_space_reconstruction': optimize_programs.PhaseSpaceReconstructionOptimizer,
    }

    QUAD_SET_PROGRAMS = {
        'manual': set_programs.ManualQuadSet,
        'geecs_python_api': set_programs.GEECSPythonAPIQuadSet,
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

        self.quad_scan_program: scan_programs.QuadScanProgram = self.QUAD_SCAN_PROGRAMS[quad_scan_method]()
        self.quad_optimize_program: optimize_programs.QuadOptimizeProgram = self.QUAD_OPTIMIZE_PROGRAMS[quad_optimize_method]()
        self.quad_set_program: set_programs.QuadSetProgram = self.QUAD_SET_PROGRAMS[quad_set_method]()

    def run_one_iteration(self):
        quad_scan_images: list[QuadScanImage] = self.quad_scan_program.run_quad_scan()
        optimal_quad_configuration: QuadConfiguration = self.quad_optimize_program.run_optimization(quad_scan_images)
        self.quad_set_program.set_quad_properties(optimal_quad_configuration)

    def run(self):
        self.run_one_iteration()

if __name__ == "__main__":
    qsqo = QuadScanQuadOptimization()
    qsqo.run()
