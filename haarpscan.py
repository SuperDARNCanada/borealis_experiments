#!/usr/bin/python

"""
haarpscan
~~~~~~~~~
A one-off experiment for a collaboration with HAARP ran June 2021 at CLY.
Run beams 2, 3, 4, 5, 6 at Clyde. Beam 4 range gate 72 overlaps with Gakona, AK

:copyright: 2021 SuperDARN Canada
:author: Kevin Krieger
"""

import borealis_experiments.superdarn_common_fields as scf
from utils.experiment_prototype import ExperimentPrototype


class HAARPScan(ExperimentPrototype):
    cpid = 3530

    def __init__(self, **kwargs):
        """
        kwargs:

        freq: int

        """
        super().__init__()

        if scf.config.scan_direction == "forward":
            beams_to_use = [2, 3, 4, 5, 6, 2, 3, 4, 5, 6, 2, 3, 4, 5, 6, 2]
        else:
            beams_to_use = [6, 5, 4, 3, 2, 6, 5, 4, 3, 2, 6, 5, 4, 3, 2, 6]

        # default frequency set here
        freq = kwargs.get("freq", scf.COMMON_MODE_FREQ_1)

        self.add_slice(
            {  # slice_id = 0, there is only one slice.
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": 3500,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "tx_beam_order": beams_to_use,
                "rx_beam_order": beams_to_use,
                "scanbound": [i * 3.5 for i in range(len(beams_to_use))],  # 1 min scan
                "freq": freq,  # kHz
                "acf": True,
                "xcf": True,  # cross-correlation processing
                "acfint": True,  # interferometer acfs
            }
        )
