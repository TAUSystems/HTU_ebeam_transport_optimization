""" Programs that optimize quadrupole magnet parameters, for use in QuadScanQuadOptimization
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pathlib import Path
import shutil
import subprocess
import tempfile

from ..types import QuadScanImage, QuadConfiguration, TwissParameters

from rsbeams.rsdata.SDDS import readSDDS

from .. import ureg

if TYPE_CHECKING:
    import numpy as np
    from ..types import Measurement, OptimalParameters

class QuadOptimizeProgram:
    """Abstract base class for a program that calculates optimal quadrupole configuration
    """
    def __init__(self):
        pass

    def run_optimization(self, measurement: Measurement) -> OptimalParameters:
        raise NotImplementedError("Derived class should implement run_optimization()")

class ElegantOptimizer(QuadOptimizeProgram):
    """ Use elegant to optimize quadrupole settings 
    
    Calculates quadrupole settings that will produce bunches with desired Twiss
    parameters

    """
    def __init__(self):
        super.__init__()
    
    def run_optimization(self, twiss_parameters: TwissParameters) -> QuadConfiguration:
        
        # We copy the elegant files to a temporary directory to prevent the output 
        # files, which are written to the same directory, from cluttering it. 
        with tempfile.TemporaryDirectory() as temp_dir:
            shutil.copytree(Path(__file__).parent / 'optimize_elegant_files', temp_dir)
            
            # The HTU_back2matching.ele file contains placeholders for the Twiss 
            # parameters measured in the quad scan. They are passed in through 
            # -macro arguments to elegant
            macros = [f"-macro={ele_file_tag}={value:.6e}" for ele_file_tag, value in 
                      [('quad_scan_beta_x', twiss_parameters.beta_x.m_as('meter/radian')),
                       ('quad_scan_beta_y', twiss_parameters.beta_y.m_as('meter/radian')),
                       ('quad_scan_alpha_x', float(twiss_parameters.alpha_x)),
                       ('quad_scan_alpha_y', float(twiss_parameters.alpha_y)),
                      ]
                     ]

            subprocess.run(['elegant', 'HTU_back2matching.ele'] + macros, cwd=temp_dir)

            # Get optimized parameters
            elegant_parameter_output_sdds_file: readSDDS = readSDDS(Path(temp_dir) / 'HTU_back2matching.step2.param')
            elegant_parameter_output_sdds_file.read()
            
            # output data is a record array with fields ElementName, ElementParameter
            # ParameterValue, ParameterValueString, ElementType, ElementOccurrence, 
            # ElementGroup
            elegant_parameter_output_data: np.ndarray = elegant_parameter_output_sdds_file.columns[0]
            elegant_parameter_output_dict = {
                (element_name, element_parameter): parameter_value
                for element_name, element_parameter, parameter_value, parameter_value_string, element_type, element_occurrence, element_group
                in elegant_parameter_output_data
            }

            return QuadConfiguration(
                PMQ1_loc = elegant_parameter_output_dict[('SRCTOPMQ1', 'L')] * ureg.meter,
                PMQ2_loc = 0.0 * ureg.meter,
                PMQ3_loc = 0.0 * ureg.meter,
                EMQ1_k1 = elegant_parameter_output_dict[('EMQ1H', 'K1')] * ureg.meter**-2,
                EMQ2_k1 = elegant_parameter_output_dict[('EMQ2V', 'K1')] * ureg.meter**-2,
                EMQ3_k1 = elegant_parameter_output_dict[('EMQ3H', 'K1')] * ureg.meter**-2,
            )


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
