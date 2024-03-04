#!/usr/bin/python

"""
    twofsound
    ~~~~~~~~~
    Standard operating Borealis experiment. Alternates transmitting in two different frequencies.

    :copyright: 2023 SuperDARN Canada
"""

import copy

from experiment_prototype.experiment_prototype import ExperimentPrototype
import borealis_experiments.superdarn_common_fields as scf


class TuningSound(ExperimentPrototype):

    def __init__(self, **kwargs):
        cpid = 404  # Tune not found

        if scf.IS_FORWARD_RADAR:
            beams_to_use = scf.STD_16_FORWARD_BEAM_ORDER
        else:
            beams_to_use = scf.STD_16_REVERSE_BEAM_ORDER

        if scf.options.site_id in ["cly", "rkn", "inv"]:
            num_ranges = scf.POLARDARN_NUM_RANGES
        if scf.options.site_id in ["sas", "pgr", "lab"]:
            num_ranges = scf.STD_NUM_RANGES

        tx_freq_1 = scf.COMMON_MODE_FREQ_1
        tx_freq_2 = scf.COMMON_MODE_FREQ_2

        if kwargs:
            if 'freq1' in kwargs.keys():
                tx_freq_1 = int(kwargs['freq1'])
            if 'freq2' in kwargs.keys():
                tx_freq_2 = int(kwargs['freq2'])

        rxctrfreq = txctrfreq = (tx_freq_1 + tx_freq_2) / 2

        slice_1 = {  # slice_id = 0, the first slice
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": num_ranges,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,  # duration of an integration, in ms
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": beams_to_use,
            "tx_beam_order": beams_to_use,
            "scanbound": scf.easy_scanbound(scf.INTT_7P, beams_to_use),
            "freq": tx_freq_1,     # kHz
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
            "tuning_freq": [tx_freq_1, tx_freq_1]
        }

        slice_2 = copy.deepcopy(slice_1)
        slice_2['freq'] = tx_freq_2
        slice_2['tuning_freq'] = [tx_freq_2, tx_freq_2]

        super().__init__(cpid, txctrfreq=txctrfreq, rxctrfreq=rxctrfreq,
                         comment_string='A re-tuning (large freq diff) twofsound style experiment')

        self.add_slice(slice_1)
        self.add_slice(slice_2, interfacing_dict={0: 'SCAN'})


