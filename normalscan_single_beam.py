#!/usr/bin/python

"""
    normalscan_single_beam
    ~~~~~~~~~~~~~~~~~~~~~~
    normalscan but only using beam 3

    last scheduled 2019-12-03

    :copyright: 2019 SuperDARN Canada
"""

from borealis import ExperimentPrototype
import borealis_experiments.superdarn_common_fields as scf


class NormalscanSingleBeam(ExperimentPrototype):
    # with 7 PULSE sequence
    def __init__(self):
        cpid = 3581

        super().__init__(cpid)

        self.add_slice({  # slice_id = 0, there is only one slice.
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,  # duration of an integration, in ms
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": [2], # beam 3
            "tx_beam_order": [2],
            "freq" : scf.COMMON_MODE_FREQ_1, #kHz
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
        })
