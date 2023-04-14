#!/usr/bin/python

"""
    listening_normalscan_1
    ~~~~~~~~~~~~~~~~~~~~~~
    normalscan and listen has an appended listening integration time at the end of a full scan.
    integration times are reduced to 3s to allow time for this listening integration time.

    Normalscan with a second slice for listening on the same frequency at the end of the scan.

    :copyright: 2020 SuperDARN Canada
    :author: Marci Detwiller
"""

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype


class ListeningNormalscan1(ExperimentPrototype):

    def __init__(self):
        cpid = 3381
        super().__init__(cpid, comment_string='Normalscan with a second slice for listening on '
                                              'the same frequency at the end of the scan.')

        if scf.IS_FORWARD_RADAR:
            beams_to_use = scf.STD_16_FORWARD_BEAM_ORDER
        else:
            beams_to_use = scf.STD_16_REVERSE_BEAM_ORDER

        if scf.options.site_id in ["cly", "rkn", "inv"]:
            num_ranges = scf.POLARDARN_NUM_RANGES
        if scf.options.site_id in ["sas", "pgr", "lab"]:
            num_ranges = scf.STD_NUM_RANGES

        self.add_slice({  # slice_id = 0, added first
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": num_ranges,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": 3000,  # duration of an integration, in ms
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": beams_to_use,
            "tx_beam_order": beams_to_use,
            # scanbound ends at 48s.
            "scanbound": [i * 3.0 for i in range(len(beams_to_use))],
            "freq" : scf.COMMON_MODE_FREQ_1, #kHz
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
        })

        self.add_slice({  # slice_id = 1, receive only
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": num_ranges,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": 3000,  # duration of an integration, in ms
            "beam_angle": [0.0],  #boresite
            "rx_beam_order": [0],
            "scanbound" : [50.0],  #50th second of minute
            "freq" : scf.COMMON_MODE_FREQ_1, #kHz, same frequency but receive-only
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
            "rxonly": True,
        }, interfacing_dict={0: 'SCAN'})
