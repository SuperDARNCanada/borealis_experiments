#!/usr/bin/python

"""
cyp_noise_scan
~~~~~~~~~
CFS scan to investigate transmitting noise in Cyprus.

:copyright: 2026 SuperDARN Canada
"""

import copy

from utils.experiment_prototype import ExperimentPrototype
import borealis_experiments.superdarn_common_fields as scf


class cyp_noise_scan(ExperimentPrototype):
    cpid = 6969  # CHANGE THIS!!!

    def __init__(self, **kwargs):
        
        slice_1 = {  # slice_id = 0, the first slice
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_MS,  # duration of an integration, in ms
            "beam_angle": scf.STD_BEAM_ANGLES,
            "rx_beam_order": scf.STD_BEAM_ORDER,
            "tx_beam_order": scf.STD_BEAM_ORDER,
            "scanbound": scf.easy_scanbound(scf.INTT_MS, scf.STD_BEAM_ORDER),
            "cfs_range": [13620, 13820],
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
        }

        slice_2 = copy.deepcopy(slice_1)
        slice_3 = copy.deepcopy(slice_1)
        slice_2["cfs_range"] = [15150, 15450]
        slice_3["cfs_range"] = [16150, 16250]

        super().__init__(comment_string="Cyprus spectrum measurement test")

        self.add_slice(slice_1)
        self.add_slice(slice_2, interfacing_dict={0: "CONCURRENT"})
        self.add_slice(slice_3, interfacing_dict={0: "CONCURRENT", 1: "CONCURRENT"})
