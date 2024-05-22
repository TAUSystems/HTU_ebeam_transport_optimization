""" Programs that run a quadrupole magnet scan for use in QuadScanQuadOptimization
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..types import TwissParameters
    from geecs_python_api.controls.api_defs import ScanTag
    from pathlib import Path

from htu_scripts.analysis.quad_scan_analysis import QuadScanAnalysis
from geecs_python_api.controls.experiment.htu import HtuExp
from geecs_python_api.analysis.images.scans.scan_data import ScanData
from geecs_python_api.analysis.images.scans.scan_images import ScanImages
from geecs_python_api.tools.images.filtering import FiltersParameters

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
    camera: str = 'A3'

    emq_number = 3
    # distance from center of given emq to A3 screen
    quad_to_screen_distance = 2.126 * ureg.meter

    def __init__(self):
        super().__init__()

        self.htu = HtuExp(get_info=True)
        self.htu.connect(laser=False, jet=False, diagnostics=False, transport=True)

    def run_quad_scan(self) -> ScanTag:
        scan_path, scan_number, command_accepted, scan_timed_out = \
            self.htu.transport.quads.scan_current(self.emq_number, 1.23, 1.23)

        return scan_path

    def analyze_quad_scan(self, scan_folder: Path):
        scan_data = ScanData(scan_folder, ignore_experiment_name=self.htu.is_offline)
        scan_images = ScanImages(scan_data, self.camera)
        quad_analysis = QuadAnalysis(scan_data, scan_images, self.emq_number, fwhms_metric='median', quad_2_screen=self.quad_to_screen_distance)

        _filters = FiltersParameters(contrast=1.333, hp_median=2, hp_threshold=3., denoise_cycles=0, gauss_filter=5.,
                                    com_threshold=0.8, bkg_image=None, box=True, ellipse=False)

        # scan analysis
        # --------------------------------------------------------------------------
        path = quad_analysis.analyze(None, initial_filtering=_filters, ask_rerun=False, blind_loads=True,
                                     store_images=False, store_scalars=False, save_plots=False, save=False)
        

    def measure_twiss_parameters(self) -> TwissParameters:
        scan_path = self.run_quad_scan()
        self.analyze_quad_scan(scan_path)

