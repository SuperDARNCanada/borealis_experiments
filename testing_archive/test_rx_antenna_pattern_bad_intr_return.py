#!/usr/bin/python

"""
Experiment fault: 
    rx_antenna_pattern interferometer array is the wrong shape
Expected exception:
    Slice .* rx antenna pattern interferometer array must be the same shape as [beam_angle, antenna_count]
"""

import numpy as np

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype

### Method returns a list which will fail in check_slice()
### of ExperimentPrototype
def rx_antenna_pattern(beam_angle, freq, rx_antennas, rx_spacing, offset=0.0):
    """Sets the amplitude and phase weighting for each tx antenna as a list"""
    beam_angle_num = len(beam_angle) + int(abs(offset))
    pattern = np.array([1.0 for _ in range(len(rx_antennas) * beam_angle_num)])
    pattern = pattern.reshape((beam_angle_num, len(rx_antennas)))
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
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": [beams_to_use],
            "tx_beam_order": [0],
            "rx_antenna_pattern": rx_antenna_pattern,
            "freq": freq,  # kHz
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
        })
