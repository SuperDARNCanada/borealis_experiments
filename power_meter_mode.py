#!/usr/bin/python

"""
    power_meter_mode
    ~~~~~~~~~~~~~~~~
    For testing transmitters with Bird power meter

    :copyright: 2021 SuperDARN Canada
    :author: Kevin Krieger
"""

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
from experiment_prototype.decimation_scheme.decimation_scheme import create_default_scheme


class PowerMeterMode(ExperimentPrototype):

    def __init__(self, **kwargs):
        """
        kwargs:

        freq: int

        """
        cpid = 3580
        super().__init__(cpid)

        # default frequency set here
        freq = scf.COMMON_MODE_FREQ_1
        
        if kwargs:
            if 'freq' in kwargs.keys():
                freq = kwargs['freq']
        
        print('Frequency set to {}'.format(freq))   # TODO: Log

        self.add_slice({  # slice_id = 0, there is only one slice.
            "pulse_sequence": [0],
            "tau_spacing": 300,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": 1,
            "first_range": 0,
            "intt": 4000,  # duration of an integration, in ms
            "beam_angle": [0.0],
            "tx_beam_order": [0],
            "rx_beam_order": [0],
            #"scanbound": [i * 3.5 for i in range(len(beams_to_use))], #1 min scan
            "freq" : freq, #kHz
            "acf": False,
            "xcf": False,  # cross-correlation processing
            "acfint": False,  # interferometer acfs
            "decimation_scheme": create_default_scheme(),
        })

