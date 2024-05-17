#!/usr/bin/python

"""
Experiment fault:
    pulse_phase_offset return value does not have shape equal to (num_pulses,)
"""

import numpy as np

import borealis_experiments.superdarn_common_fields as scf
from borealis import ExperimentPrototype
from borealis import decimation_scheme as dm
from pydantic import ValidationError


def phase_encode(beam_iter, sequence_num, num_pulses):
    return np.random.uniform(-180.0, 180, num_pulses-1)     # length is not num_pulses


class TestExperiment(ExperimentPrototype):

    def __init__(self):
        cpid = 1

        default_slice = {  # slice_id = 0, the first slice
            "pulse_sequence": scf.SEQUENCE_8P,
            "tau_spacing": scf.TAU_SPACING_8P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_8P,
            "beam_angle": [1.75],
            "rx_beam_order": [0],
            "tx_beam_order": [0],
            "freq": 13100,
            "decimation_scheme": dm.create_default_scheme(),
            "pulse_phase_offset": phase_encode
        }

        super().__init__(cpid)

        self.add_slice(default_slice)

    @classmethod
    def error_message(cls):
        return ValidationError, "pulse_phase_offset\n" \
                                "  Slice 0 Phase encoding return dimension must be equal to number of pulses " \
                                "\(type=value_error\)"