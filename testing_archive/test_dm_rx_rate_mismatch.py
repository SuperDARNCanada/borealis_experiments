#!/usr/bin/python

"""
Experiment fault:
    rx_bandwidth does not match input data rate of DecimationScheme
"""

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
from experiment_prototype.experiment_utils.decimation_scheme import create_default_scheme
from pydantic import ValidationError


class TestExperiment(ExperimentPrototype):

    def __init__(self):
        cpid = 1

        ### Should fail due to being too large
        super(TestExperiment, self).__init__(cpid, rx_bandwidth=1e6)

        if scf.IS_FORWARD_RADAR:
            beams_to_use = scf.STD_16_FORWARD_BEAM_ORDER
        else:
            beams_to_use = scf.STD_16_REVERSE_BEAM_ORDER

        if scf.options.site_id in ["cly", "rkn", "inv"]:
            num_ranges = scf.POLARDARN_NUM_RANGES
        if scf.options.site_id in ["sas", "pgr"]:
            num_ranges = scf.STD_NUM_RANGES

        slice_1 = {  # slice_id = 0, there is only one slice.
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": num_ranges,
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
        return ValidationError, \
            "decimation_scheme input data rate 5000000.0 does not match rx_bandwidth 1000000.0"