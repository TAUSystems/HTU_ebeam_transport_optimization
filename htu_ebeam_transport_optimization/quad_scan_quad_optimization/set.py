""" Programs that set property values on the quadrupole magnets
"""

from __future__ import annotations

class QuadSetProgram:
    """Base class for a program that sets property values of quadrupoles
    """
    def __init__(self):
        pass

    def set_quad_properties(self):
        raise NotImplementedError("set_quad_properties() should be implemented by derived class")

class ManualQuadScan(QuadSetProgram):
    """ Requests an operator to set properties
    """
    def __init__(self):
        super().__init__()
    
    def set_quad_properties(self):
        pass

class GEECSPythonAPIQuadScan(QuadSetProgram):
    """ Uses GEECS-PythonAPI to set property values
    """
    def __init__(self):
        super().__init__()

    def set_quad_properties(self):
        pass

