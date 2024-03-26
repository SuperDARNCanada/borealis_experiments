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


class TuningTest(ExperimentPrototype):

    def __init__(self, **kwargs):
        cpid = 3504  # Tune not found

        if scf.IS_FORWARD_RADAR:
            beams_to_use = scf.STD_16_FORWARD_BEAM_ORDER
        else:
            beams_to_use = scf.STD_16_REVERSE_BEAM_ORDER

        if scf.options.site_id in ["cly", "rkn", "inv"]:
            num_ranges = scf.POLARDARN_NUM_RANGES
        if scf.options.site_id in ["sas", "pgr", "lab"]:
            num_ranges = scf.STD_NUM_RANGES

        tx_freq = scf.COMMON_MODE_FREQ_1
        center_freq = tx_freq - 1500

        if kwargs:
            if 'freq' in kwargs.keys():
                tx_freq = int(kwargs['freq'])

        slice_1 = {  # slice_id = 0, the first slice
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": num_ranges,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,  # duration of an integration, in ms
            "beam_angle": [0.0],
            "rx_beam_order": [0],
            "tx_beam_order": [0],
            "freq": tx_freq,     # kHz
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
            "rxctrfreq": center_freq,
            "txctrfreq": center_freq,
        }

        super().__init__(cpid, comment_string='An N200 re-tuning test')

        slice_list = []
        freq_offsets = [500]

        # Move only tx center freq
        for offset in freq_offsets:
            new_slice = copy.deepcopy(slice_1)
            new_slice['txctrfreq'] = tx_freq + offset
            slice_list.append(new_slice)

        # Move only rx center freq
        for offset in freq_offsets:
            new_slice = copy.deepcopy(slice_1)
            new_slice['rxctrfreq'] = tx_freq + offset
            slice_list.append(new_slice)

        # Move both center freqs
        for offset in freq_offsets:
            new_slice = copy.deepcopy(slice_1)
            new_slice['txctrfreq'] = tx_freq + offset
            new_slice['rxctrfreq'] = tx_freq + offset
            slice_list.append(new_slice)

        interfacing_dict = {}
        for ind in range(len(slice_list)):
            if ind == 0:
                self.add_slice(slice_list[ind])
            else:
                interfacing_dict[int(ind - 1)] = 'AVEPERIOD'
                self.add_slice(slice_list[ind], interfacing_dict=interfacing_dict)


