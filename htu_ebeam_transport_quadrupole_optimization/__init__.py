# Common UnitRegistry to use throughout this package
from pint import UnitRegistry
ureg = UnitRegistry()
Q_ = Quantity = ureg.Quantity
