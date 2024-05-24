from typing import NamedTuple, NewType, Annotated, Any
from numpy.typing import NDArray

# Measurement = NewType("Measurement", Any)
OptimalParameters = NewType("OptimalParameters", Any)

from pint import Quantity

DimensionlessQuantity = NewType("DimensionlessQuantity", Annotated[Quantity, ''])
LengthQuantity = NewType("LengthQuantity", Annotated[Quantity, '[length]'])
InverseLengthSquaredQuantity = NewType("InverseLengthSquaredQuantity", Annotated[Quantity, '[length]^-2'])
LengthPerAngleQuantity = NewType("LengthPerAngleQuantity", Annotated[Quantity, '[length] / [angle]'])
LengthAngleQuantity = NewType("LengthAngleQuantity", Annotated[Quantity, '[length] * [angle]'])
CurrentQuantity = NewType("CurrentQuantity", Annotated[Quantity, '[current]'])

# a run_quad_scan() result is a list of QuadScanImage 
class QuadScanImage(NamedTuple):
    image: NDArray
    EMQ3_k1: InverseLengthSquaredQuantity
    resolution_x: LengthQuantity
    resolution_y: LengthQuantity

# a run_optimization() result is quadrupole parameters
class QuadConfiguration(NamedTuple):
    PMQ1_loc: LengthQuantity
    PMQ2_loc: LengthQuantity
    PMQ3_loc: LengthQuantity
    EMQ1_k1: InverseLengthSquaredQuantity
    EMQ2_k1: InverseLengthSquaredQuantity
    EMQ3_k1: InverseLengthSquaredQuantity

class TwissParameters(NamedTuple):
    beta_x: LengthPerAngleQuantity
    beta_y: LengthPerAngleQuantity
    alpha_x: float | DimensionlessQuantity
    alpha_y: float | DimensionlessQuantity
    emittance_x: LengthAngleQuantity
    emittance_y: LengthAngleQuantity

class Measurement(NamedTuple):
    pass

class QuadScanMeasurement(Measurement):
    pass

class GEECSPythonAPITwissQuadScanMeasurement(QuadrupoleOptimizerMeasurement):
    twiss_parameters: TwissParameters
    emq3_current: CurrentQuantity
