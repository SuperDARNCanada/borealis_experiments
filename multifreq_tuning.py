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
        tx_freq_2 = scf.COMMON_MODE_FREQ_1 - 1900
        tx_freq_3 = scf.COMMON_MODE_FREQ_2
        tx_freq_4 = scf.COMMON_MODE_FREQ_2 + 2500

        if kwargs:
            if 'freq1' in kwargs.keys():
                tx_freq_1 = int(kwargs['freq1'])
            if 'freq2' in kwargs.keys():
                tx_freq_2 = int(kwargs['freq2'])
            if 'freq3' in kwargs.keys():
                tx_freq_3 = int(kwargs['freq3'])
            if 'freq4' in kwargs.keys():
                tx_freq_4 = int(kwargs['freq4'])

        freqs = [tx_freq_1, tx_freq_2, tx_freq_3, tx_freq_4]
        freqs.sort()
        freq1, freq2, freq3, freq4 = freqs

        center_freq1 = (freq1 + freq2) / 2
        center_freq2 = (freq3 + freq4) / 2

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
            "freq": freq1,     # kHz
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
            "rxctrfreq": center_freq1,
            "txctrfreq": center_freq1
        }

        slice_2 = copy.deepcopy(slice_1)
        slice_2['freq'] = freq2

        slice_3 = copy.deepcopy(slice_1)
        slice_3['freq'] = freq3
        slice_3['rxctrfreq'] = center_freq2
        slice_3['txctrfreq'] = center_freq2

        slice_4 = copy.deepcopy(slice_3)
        slice_4['freq'] = freq4

        super().__init__(cpid, comment_string='A re-tuning (large freq diff) twofsound style experiment')

        self.add_slice(slice_1)
        self.add_slice(slice_3, interfacing_dict={0: 'AVEPERIOD'})
        self.add_slice(slice_2, interfacing_dict={0: 'SCAN', 1:'SCAN'})
        self.add_slice(slice_4, interfacing_dict={0:'SCAN', 1:'SCAN', 2:'AVEPERIOD'})

