""" Programs that optimize quadrupole magnet parameters, for use in QuadScanQuadOptimization
"""

from __future__ import annotations

class QuadOptimizeProgram:
    """Abstract base class for a program that calculates optimal quadrupole configuration
    """
    def __init__(self):
        pass

    def run_optimization(self):
        raise NotImplementedError("Derived class should implement run_optimization()")
    

class ElegantOptimizer(QuadOptimizeProgram):
    """ Use elegant to optimize quadrupole settings.
    """
    def __init__(self):
        super.__init__()
    
    def run_optimization(self):
        pass


class PhaseSpaceReconstructionOptimizer(QuadOptimizeProgram):
    """ Use full phase space reconstruction and tracking to optimize quadrupole configuration
    """
    def __init__(self):
        super.__init__()
    
    def run_optimization(self):
        pass

