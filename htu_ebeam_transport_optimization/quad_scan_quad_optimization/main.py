""" Quad Scan Quad Optimization

The main program that optimizes quadrupole strength and placement by 
iteratively running a quadrupole scan to determine Twiss parameters, optimizing
magnet settings, and setting the quadrupoles with new values.

"""

from __future__ import annotations
from typing import Type

class QuadScanQuadOptimization:
    """ Program that iteratively runs the Quad optimization process
    """
    def __init__(self, 
                 quad_scan_program: Type|str = 'manual',
                 quad_optimize_program: Type|str = 'elegant',
                 quad_set_program: Type|str = 'manual',
                ): 
        """
        Parameters
        ----------
        quad_scan_program : Type | str, optional
            _description_, by default 'manual'
        quad_optimize_program : Type | str, optional
            _description_, by default 'elegant'
        quad_set_program : Type | str, optional
            _description_, by default 'manual'
        """

    def run(self):
        pass


if __name__ == "__main__":
    qsqo = QuadScanQuadOptimization()
    qsqo.run()
