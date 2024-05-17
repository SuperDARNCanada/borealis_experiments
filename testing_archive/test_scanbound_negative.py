#!/usr/bin/python

"""
Experiment fault:
    scanbound containing negative values
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
            "rx_beam_order": beams_to_use,
            "tx_beam_order": beams_to_use,
            "scanbound": [i * -3.5 for i in range(len(beams_to_use))],  ### Negative values, should fail
            "freq" : scf.COMMON_MODE_FREQ_1, #kHz
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
            "decimation_scheme": dm.create_default_scheme(),
        }
        self.add_slice(slice_1)

    @classmethod
    def error_message(cls):
        return ValidationError, "scanbound -> 1\n" \
                                "  ensure this value is greater than or equal to 0 " \
                                "\(type=value_error.number.not_ge; limit_value=0\)\n" \
                                "scanbound -> 2\n" \
                                "  ensure this value is greater than or equal to 0 " \
                                "\(type=value_error.number.not_ge; limit_value=0\)\n" \
                                "scanbound -> 3\n" \
                                "  ensure this value is greater than or equal to 0 " \
                                "\(type=value_error.number.not_ge; limit_value=0\)\n" \
                                "scanbound -> 4\n" \
                                "  ensure this value is greater than or equal to 0 " \
                                "\(type=value_error.number.not_ge; limit_value=0\)\n" \
                                "scanbound -> 5\n" \
                                "  ensure this value is greater than or equal to 0 " \
                                "\(type=value_error.number.not_ge; limit_value=0\)\n" \
                                "scanbound -> 6\n" \
                                "  ensure this value is greater than or equal to 0 " \
                                "\(type=value_error.number.not_ge; limit_value=0\)\n" \
                                "scanbound -> 7\n" \
                                "  ensure this value is greater than or equal to 0 " \
                                "\(type=value_error.number.not_ge; limit_value=0\)\n" \
                                "scanbound -> 8\n" \
                                "  ensure this value is greater than or equal to 0 " \
                                "\(type=value_error.number.not_ge; limit_value=0\)\n" \
                                "scanbound -> 9\n" \
                                "  ensure this value is greater than or equal to 0 " \
                                "\(type=value_error.number.not_ge; limit_value=0\)\n" \
                                "scanbound -> 10\n" \
                                "  ensure this value is greater than or equal to 0 " \
                                "\(type=value_error.number.not_ge; limit_value=0\)\n" \
                                "scanbound -> 11\n" \
                                "  ensure this value is greater than or equal to 0 " \
                                "\(type=value_error.number.not_ge; limit_value=0\)\n" \
                                "scanbound -> 12\n" \
                                "  ensure this value is greater than or equal to 0 " \
                                "\(type=value_error.number.not_ge; limit_value=0\)\n" \
                                "scanbound -> 13\n" \
                                "  ensure this value is greater than or equal to 0 " \
                                "\(type=value_error.number.not_ge; limit_value=0\)\n" \
                                "scanbound -> 14\n" \
                                "  ensure this value is greater than or equal to 0 " \
                                "\(type=value_error.number.not_ge; limit_value=0\)\n" \
                                "scanbound -> 15\n" \
                                "  ensure this value is greater than or equal to 0 " \
                                "\(type=value_error.number.not_ge; limit_value=0\)"
