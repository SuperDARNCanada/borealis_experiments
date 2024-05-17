#!/usr/bin/python

"""
Experiment fault: 
    rx_beam_order list values not lists or integers
"""

import borealis_experiments.superdarn_common_fields as scf
from borealis import ExperimentPrototype
from borealis import decimation_scheme as dm
from pydantic import ValidationError


class TestExperiment(ExperimentPrototype):

    def __init__(self):
        cpid = 1
        super(TestExperiment, self).__init__(cpid)

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
            "rx_beam_order": ['0', '1', '2', '3'],  ### not list of lists or list of integers
            "tx_beam_order": [0, 1, 2, 3],
            "scanbound": [i * 3.5 for i in range(len(beams_to_use))], #1 min scan
            "freq" : scf.COMMON_MODE_FREQ_1, #kHz
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
            "decimation_scheme": dm.create_default_scheme(),
        }
        self.add_slice(slice_1)

    @classmethod
    def error_message(cls):
        return ValidationError, "rx_beam_order -> 0\n" \
                                "  value is not a valid list \(type=type_error.list\)\n" \
                                "rx_beam_order -> 0\n" \
                                "  value is not a valid integer \(type=type_error.integer\)\n" \
                                "rx_beam_order -> 1\n" \
                                "  value is not a valid list \(type=type_error.list\)\n" \
                                "rx_beam_order -> 1\n" \
                                "  value is not a valid integer \(type=type_error.integer\)\n" \
                                "rx_beam_order -> 2\n" \
                                "  value is not a valid list \(type=type_error.list\)\n" \
                                "rx_beam_order -> 2\n" \
                                "  value is not a valid integer \(type=type_error.integer\)\n" \
                                "rx_beam_order -> 3\n" \
                                "  value is not a valid list \(type=type_error.list\)\n" \
                                "rx_beam_order -> 3\n" \
                                "  value is not a valid integer \(type=type_error.integer\)"
