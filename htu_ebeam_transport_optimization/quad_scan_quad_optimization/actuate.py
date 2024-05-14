""" Programs that set property values on the quadrupole magnets
"""

from __future__ import annotations

from ..types import QuadConfiguration

class QuadSetProgram:
    """Base class for a program that sets property values of quadrupoles
    """
    def __init__(self):
        pass

    def set_quad_properties(self, quadrupole_configuration: QuadConfiguration):
        raise NotImplementedError("set_quad_properties() should be implemented by derived class")

class ManualQuadSet(QuadSetProgram):
    """ Requests an operator to set properties
    """
    def __init__(self):
        super().__init__()
    
    def set_quad_properties(self, quadrupole_configuration: QuadConfiguration):
        pass

class GEECSPythonAPIQuadSet(QuadSetProgram):
    """ Uses GEECS-PythonAPI to set property values
    """
    def __init__(self):
        super().__init__()

    def set_quad_properties(self, quadrupole_configuration: QuadConfiguration):
        pass
