"""
pgr_haarpscan
~~~~~~~~~~~~~
Uses 4 beams westward (CCW w.r.t. boresight) of the PGR FOV to focus on the ionosphere in the direction
of the HAARP instrument in Alaska.

:copyright: 2025 SuperDARN Canada
"""

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype


class PgrHaarpscan(ExperimentPrototype):
    def __init__(self, **kwargs):
        """
        """
        cpid = 3498
        super().__init__(cpid, comment_string="Scan of beams -4 to -1 at PGR, overlooking HAARP.")

        self.add_slice({
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,
            "beam_angle": [scf.STD_16_BEAM_ANGLE[0] + i * 3.24 for i in range(-4, 0)],  # 4 beams CCW of FOV
            "rx_beam_order": [0, 1, 2, 3],
            "tx_beam_order": [0, 1, 2, 3],
            "freq" : scf.COMMON_MODE_FREQ_1,
            "acf": True,
            "xcf": True,
            "acfint": False,
        })
