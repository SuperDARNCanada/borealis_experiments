#!/usr/bin/python

"""
tauscan
~~~~~~~
A 11-pulse sequence that consists of a single pulse pulse followed by a back to back 5-pulse
Farley sequence. The analysis produces a 12-pulse ACF with no missing lags.

Last scheduled 2020-07-13

:copyright: 2020 SuperDARN Canada
:author: Keith Kotyk
"""

from utils.experiment_prototype import ExperimentPrototype
import borealis_experiments.superdarn_common_fields as scf


class Tauscan(ExperimentPrototype):
    cpid = 503

    def __init__(self):
        super().__init__(comment_string=Tauscan.__doc__)

        if scf.config.site_id == "sas":
            freq = 13150
        elif scf.config.site_id == "pgr":
            freq = 13100
        else:
            freq = 13650

        slice_1 = {
            "pulse_sequence": [0, 10, 13, 14, 19, 21, 31, 33, 38, 39, 42],
            "tau_spacing": 3000,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": 100,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": 7300,  # duration of an integration, in ms
            "beam_angle": scf.STD_BEAM_ANGLES,
            "rx_beam_order": scf.STD_BEAM_ORDER,
            "tx_beam_order": scf.STD_BEAM_ORDER,
            "scanbound": scf.easy_scanbound(7400, scf.STD_BEAM_ORDER),
            "freq": freq,  # kHz
            "acf": True,
            "xcf": True,
            "acfint": True,
            "comment": Tauscan.__doc__,
        }

        self.add_slice(slice_1)
