""" Programs that run a quadrupole magnet scan for use in QuadScanQuadOptimization
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..types import TwissParameters

class QuadScanProgram:
    """Base class for a program that runs a quadrupole magnet scan
    """
    def __init__(self):
        pass

    def measure_twiss_parameters(self) -> TwissParameters:
        raise NotImplementedError("run_quad_scan() should be implemented by derived class")

class ManualQuadScan(QuadScanProgram):
    """ Requests an operator to run a quadrupole magnet scan
    """
    def __init__(self):
        super().__init__()
    
    def measure_twiss_parameters(self) -> TwissParameters:
        pass

class GEECSPythonAPIQuadScan(QuadScanProgram):
    """ Uses GEECS-PythonAPI to run a quadrupole magnet scan
    """
    def __init__(self):
        super().__init__()

    def measure_twiss_parameters(self) -> TwissParameters:
        pass

