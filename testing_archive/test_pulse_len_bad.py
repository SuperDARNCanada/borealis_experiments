#!/usr/bin/python

"""
Experiment fault: 
    pulse_len invalid
"""

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
from experiment_prototype.experiment_utils.decimation_scheme import create_default_scheme
from pydantic import ValidationError


class TestExperiment(ExperimentPrototype):

    def __init__(self):
        cpid = 1
        super().__init__(cpid)

        beams_to_use = scf.STD_16_FORWARD_BEAM_ORDER

        slice_1 = {  # slice_id = 0, there is only one slice.
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM + 1,  ### pulse_len must be the same as 1/output_rx_rate (within floating point error)
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": 3500,  # duration of an integration, in ms
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": beams_to_use,
            "tx_beam_order": beams_to_use,
            "scanbound": [i * 3.5 for i in range(len(beams_to_use))], #1 min scan
            "freq" : scf.COMMON_MODE_FREQ_1, #kHz
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
            "decimation_scheme": create_default_scheme(),
        }
        self.add_slice(slice_1)

    @classmethod
    def error_message(cls):
        return ValidationError, "For an experiment slice with real-time acfs, pulse length must be equal \(within 1 " \
                                "us\) to 1/output_rx_rate to make acfs valid. Current pulse length is 301 us, output" \
                                " rate is 3333.333 Hz. Slice: 0 \(type=value_error\)"
