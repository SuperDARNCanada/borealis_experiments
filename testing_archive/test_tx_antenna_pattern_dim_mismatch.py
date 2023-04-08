#!/usr/bin/python

"""
Experiment fault:
    tx_antenna_pattern dimension mismatch with number of main antennas
Expected exception:
    Slice .* tx antenna pattern return 2nd dimension \(.*\) must be equal to number of main antennas \(.*\)
"""

import numpy as np

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
from experiment_prototype.decimation_scheme.decimation_scheme import create_default_scheme
from pydantic import ValidationError


### pattern second dimension is not equal to num_main_antennas, this will fail in check_slice()
### of ExperimentPrototype
def tx_antenna_pattern(tx_freq_khz, tx_antennas, antenna_spacing):
    """Sets the amplitude and phase weighting for each tx antenna"""
    pattern = np.array([1.0 for _ in range(len(tx_antennas)-1)]).reshape((1, len(tx_antennas)-1))
    return pattern


class TxAntennaPatternTest(ExperimentPrototype):

    def __init__(self, **kwargs):
        """
        kwargs:

        freq: int

        """
        cpid = 12345
        super().__init__(cpid)

        beams_to_use = scf.STD_16_FORWARD_BEAM_ORDER

        if scf.options.site_id in ["cly", "rkn", "inv"]:
            num_ranges = scf.POLARDARN_NUM_RANGES
        if scf.options.site_id in ["sas", "pgr"]:
            num_ranges = scf.STD_NUM_RANGES

        # default frequency set here
        freq = scf.COMMON_MODE_FREQ_1

        if kwargs:
            if 'freq' in kwargs.keys():
                freq = kwargs['freq']

        self.add_slice({  # slice_id = 0, there is only one slice.
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": num_ranges,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,  # duration of an integration, in ms
            "tx_antenna_pattern": tx_antenna_pattern,
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": [beams_to_use],
            "tx_beam_order": [0],
            "freq": freq,  # kHz
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
            "decimation_scheme": create_default_scheme(),
        })

    @classmethod
    def error_message(cls):
        return ValidationError, \
            "Slice 0 tx antenna pattern return 2nd dimension \(15\) must be equal to number of main antennas \(16\)"
