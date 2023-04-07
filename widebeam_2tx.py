#!/usr/bin/python

"""
    widebeam_2tx
    ~~~~~~~~~~~~
    A widebeam mode that utilizes transmitters 7 and 8 only. The mode has zero phase (no beams) and
    receives on all antennas. There is no scan boundary, it simply sounds for 3.5 seconds at a time.
    It does not generate correlations and only produces antennas_iq data.

    Based on beam pattern analysis by Dr. Pasha Ponomarenko Nov 2021

    :copyright: 2022 SuperDARN Canada
    :author: Remington Rohel
"""

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
from experiment_prototype.decimation_scheme.decimation_scheme import create_default_scheme


class Widebeam_2tx(ExperimentPrototype):

    def __init__(self, **kwargs):
        """
        kwargs:

        freq: int

        """
        cpid = 3711
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
            "intt": scf.INTT_7P,  # duration of an integration, in ms
            "beam_angle": [0],
            "rx_beam_order": [0],
            "tx_beam_order": [0],
            "freq": freq,  # kHz
            "tx_antennas": [7, 8],  # Using two tx antennas from the middle of array
            "align_sequences": True,
            "scanbound": [i * scf.INTT_7P * 1e-3 for i in range(len(scf.STD_16_BEAM_ANGLE))],
            "decimation_scheme": create_default_scheme(),
        })

