#!/usr/bin/python

"""
    widebeam_3tx
    ~~~~~~~~~~~~
    A widebeam mode that utilizes transmitters 6 7 and 8 only. The mode has zero phase (no beams)
    and receives on all antennas. There is no scan boundary, it simply sounds for 3.5 seconds at a
    time. It does not generate correlations and only produces antennas_iq data.

    Based on beam pattern analysis by Dr. Pasha Ponomarenko Nov 2021

    :copyright: 2022 SuperDARN Canada
    :author: Remington Rohel
"""

import borealis_experiments.superdarn_common_fields as scf
from borealis import ExperimentPrototype


class Widebeam_3tx(ExperimentPrototype):

    def __init__(self, **kwargs):
        """
        kwargs:

        freq: int

        """
        cpid = 3710
        super().__init__(cpid)

        if scf.options.site_id in ["cly", "rkn", "inv"]:
            num_ranges = scf.POLARDARN_NUM_RANGES
        if scf.options.site_id in ["sas", "pgr", "lab"]:
            num_ranges = scf.STD_NUM_RANGES

        # default frequency set here
        freq = scf.COMMON_MODE_FREQ_1
        
        if kwargs:
            if 'freq' in kwargs.keys():
                freq = kwargs['freq']
        
        print('Frequency set to {}'.format(freq))   # TODO: Log

        self.add_slice({  # slice_id = 0, there is only one slice.
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": num_ranges,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": 3500,  # duration of an integration, in ms
            "beam_angle": [0],
            "rx_beam_order": [0],
            "tx_beam_order": [0],
            "freq": freq,  # kHz
            "tx_antennas": [6, 7, 8],  # Using three tx antennas from near the middle of array
        })

