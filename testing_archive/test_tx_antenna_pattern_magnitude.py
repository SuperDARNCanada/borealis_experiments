#!/usr/bin/python

"""
Experiment fault: 
    tx_antenna_pattern magnitude too large
Expected exception:
    Slice .* tx antenna pattern return must not have any values with a magnitude greater than 1
"""

import numpy as np

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype

### One of the pattern's elements' magnitudes is > 1.0, this will fail in check_slice()
### of ExperimentPrototype
def tx_antenna_pattern(tx_freq_khz, tx_antennas, antenna_spacing):
    """Sets the amplitude and phase weighting for each tx antenna"""
    pattern = np.array([1.0 for _ in range(len(tx_antennas))]).reshape((1, len(tx_antennas)))
    pattern[0, 0] = 1.01
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

        self.printing('Frequency set to {}'.format(freq))

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
        })

