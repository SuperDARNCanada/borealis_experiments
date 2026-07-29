#!/usr/bin/python

"""
narrow_wide_comparison
~~~~~~~~~~~~~~~~~~~~~~
This mode is a comparison between the transmission characteristics of full_fov.py and
normalscan.py, running on one frequency but interleaving the two transmissions each averaging
period. The first pulse in each sequence starts on the 0.1 second boundaries, to enable bistatic
listening on other radars.

:copyright: 2022 SuperDARN Canada
:author: Remington Rohel
"""

import copy
import numpy as np

import borealis_experiments.superdarn_common_fields as scf
from borealis_experiments.superdarn_common_fields import STD_SCANBOUND
from utils.experiment_prototype import ExperimentPrototype


def boresight(frequency_khz, tx_antennas, antenna_spacing_m):
    """tx_antenna_pattern function for boresight transmission."""
    num_antennas = scf.config.main_antenna_count
    pattern = np.zeros((1, num_antennas), dtype=np.complex64)
    pattern[0, tx_antennas] = 1.0 + 0.0j
    return pattern


class FullFOVComparison(ExperimentPrototype):
    cpid = 3812

    def __init__(self, **kwargs):
        """
        kwargs:

        freq: int, kHz

        """

        super().__init__()

        # default frequency set here
        freq = kwargs.get("freq", scf.COMMON_MODE_FREQ_1)

        slice_0 = {  # slice_id = 0
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_MS,  # duration of an integration, in ms
            "beam_angle": scf.STD_BEAM_ANGLES,
            "rx_beam_order": [[i for i in range(len(scf.STD_BEAM_ANGLES))]],
            "tx_beam_order": [0],  # only one pattern
            "tx_antenna_pattern": scf.easy_widebeam,
            "freq": freq,  # kHz
            "align_sequences": True,  # align start of sequence to tenths of a second
            "scanbound": STD_SCANBOUND,
            "wait_for_first_scanbound": False,
        }

        slice_1 = copy.deepcopy(slice_0)
        slice_1["tx_antenna_pattern"] = boresight

        self.add_slice(slice_0)
        self.add_slice(slice_1, interfacing_dict={0: "AVEPERIOD"})
