#!/usr/bin/python

"""
twofsound
~~~~~~~~~
Standard operating Borealis experiment. Alternates transmitting in two different frequencies.

:copyright: 2023 SuperDARN Canada
"""

import copy

from utils.experiment_prototype import ExperimentPrototype
import borealis_experiments.superdarn_common_fields as scf


class Twofsound(ExperimentPrototype):
    cpid = 3503

    def __init__(self, **kwargs):

        tx_freq_1 = int(kwargs.get("freq1", scf.COMMON_MODE_FREQ_1))
        tx_freq_2 = int(kwargs.get("freq2", scf.COMMON_MODE_FREQ_2))

        rxctrfreq = txctrfreq = int((tx_freq_1 + tx_freq_2) / 2)

        slice_1 = {  # slice_id = 0, the first slice
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_MS,  # duration of an integration, in ms
            "beam_angle": scf.STD_BEAM_ANGLES,
            "rx_beam_order": scf.STD_BEAM_ORDER,
            "tx_beam_order": scf.STD_BEAM_ORDER,
            "scanbound": scf.STD_SCANBOUND,
            "freq": tx_freq_1,  # kHz
            "txctrfreq": txctrfreq,
            "rxctrfreq": rxctrfreq,
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
        }

        slice_2 = copy.deepcopy(slice_1)
        slice_2["freq"] = tx_freq_2

        super().__init__(comment_string="Twofsound classic scan-by-scan")

        self.add_slice(slice_1)

        self.add_slice(slice_2, interfacing_dict={0: "SCAN"})
