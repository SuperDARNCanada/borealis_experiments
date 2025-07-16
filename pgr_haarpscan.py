"""
pgr_haarpscan
~~~~~~~~~~~~~
Uses 4 beams westward (CCW w.r.t. boresight) of the PGR FOV to focus on the ionosphere in the direction
of the HAARP instrument in Alaska.

:copyright: 2025 SuperDARN Canada
"""

import copy
import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype


class PgrHaarpscan(ExperimentPrototype):
    def __init__(self, **kwargs):
        """
        """
        cpid = 3498
        super().__init__(cpid, comment_string="Scan of beams -4 to 11 at PGR, overlooking HAARP.")

        slice_0 = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,
            "beam_angle": [azm - (3.24 * 4) for azm in scf.STD_16_BEAM_ANGLE],  # 4 beams CCW of FOV plus 12 most westerly beams within FOV
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq" : scf.COMMON_MODE_FREQ_1,
            "acf": True,
            "xcf": True,
            "acfint": False,
        }
        slice_1 = copy.deepcopy(slice_0)
        slice_1["freq"] = scf.COMMON_MODE_FREQ_2

        self.add_slice(slice_0)
        self.add_slice(slice_1, interfacing_dict={0: "SCAN"})
