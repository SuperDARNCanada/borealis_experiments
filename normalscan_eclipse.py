"""
normalscan
~~~~~~~~~~
Normalscan with higher operating frequency. For August 2026 solar eclipse.

:copyright: 2026 SuperDARN Canada
"""

import borealis_experiments.superdarn_common_fields as scf
from utils.experiment_prototype import ExperimentPrototype


class NormalscanEclipse(ExperimentPrototype):
    cpid = 3899

    def __init__(self, **kwargs):
        """
        kwargs:

        freq: int

        """
        super().__init__(comment_string="Cyprus August 2026 Solar Eclipse experiment")

        # default frequency set here
        freq = kwargs.get("freq", scf.COMMON_MODE_FREQ_3)   # Use higher frequency (17.5 MHz)
        

        self.add_slice(
            {  # slice_id = 0, there is only one slice.
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": scf.INTT_MS,  # duration of an integration, in ms
                "beam_angle": scf.STD_BEAM_ANGLES,
                "rx_beam_order": scf.STD_BEAM_ORDER,
                "tx_beam_order": scf.STD_BEAM_ORDER,
                "scanbound": scf.STD_SCANBOUND,
                "freq": freq,  # kHz
                #"cfs_range": [17401, 17600],
                "acf": True,
                "xcf": True,  # cross-correlation processing
                "acfint": True,  # interferometer acfs
                "wait_for_first_scanbound": False,
            }
        )
