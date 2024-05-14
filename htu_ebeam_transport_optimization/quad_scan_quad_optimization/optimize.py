""" Programs that optimize quadrupole magnet parameters, for use in QuadScanQuadOptimization
"""

from __future__ import annotations
import tempfile

from ..types import QuadScanImage, QuadConfiguration, TwissParameters

class QuadOptimizeProgram:
    """Abstract base class for a program that calculates optimal quadrupole configuration
    """
    def __init__(self):
        pass

    def run_optimization(self, quad_scan_images: list[QuadScanImage]) -> QuadConfiguration:
        raise NotImplementedError("Derived class should implement run_optimization()")

class ElegantOptimizer(QuadOptimizeProgram):
    """ Use elegant to optimize quadrupole settings 
    
    Calculates quadrupole settings that will produce bunches with desired Twiss
    parameters

    """
    def __init__(self):
        super.__init__()
    
    def _calculate_twiss_parameters(self, quad_scan_images: list[QuadScanImage]) -> TwissParameters:
        pass

    def _run_elegant_optimization(self, twiss_parameters: TwissParameters) -> QuadConfiguration:
        pass

    def run_optimization(self, quad_scan_images: list[QuadScanImage]) -> QuadConfiguration:
        twiss_parameters = self._calculate_twiss_parameters(quad_scan_images)
        return self._run_elegant_optimization(twiss_parameters)

class RSOptOptimizer(QuadOptimizeProgram):
    """ Use RSOpt to optimize quadrupole settings

    Runs optimizer whose objective is the result of elegant tracking simulations.
    """
    def __init__(self):
        super.__init__()
    
    def run_optimization(self, quad_scan_images: list[QuadScanImage]) -> QuadConfiguration:
        pass


class PhaseSpaceReconstructionOptimizer(QuadOptimizeProgram):
    """ Use full phase space reconstruction and tracking to optimize quadrupole configuration
    """
    def __init__(self):
        super.__init__()
    
    def run_optimization(self, quad_scan_images: list[QuadScanImage]) -> QuadConfiguration:
        pass
