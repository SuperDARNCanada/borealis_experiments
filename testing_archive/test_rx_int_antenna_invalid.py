#!/usr/bin/python

"""
Experiment fault:
    tx_antennas has invalid values (above and below the allowed range)
"""

import borealis_experiments.superdarn_common_fields as scf
from borealis import ExperimentPrototype
from borealis import decimation_scheme as dm
from pydantic import ValidationError


class TestExperiment(ExperimentPrototype):

    def __init__(self):
        cpid = 1
        super().__init__(cpid)

        beams_to_use = scf.STD_16_FORWARD_BEAM_ORDER
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
            "freq": scf.COMMON_MODE_FREQ_1, #kHz
            "rx_intf_antennas": [-1, 1, 2, 4],  ### antenna -1 and 4 are out of range
            "decimation_scheme": dm.create_default_scheme(),
        }
        self.add_slice(slice_1)

    @classmethod
    def error_message(cls):
        return ValidationError, "rx_intf_antennas -> 0\n" \
                                "  ensure this value is greater than or equal to 0 \(type=value_error.number.not_ge; " \
                                "limit_value=0\)\n" \
                                "rx_intf_antennas -> 3\n" \
                                "  ensure this value is less than 4 \(type=value_error.number.not_lt; limit_value=4\)"
