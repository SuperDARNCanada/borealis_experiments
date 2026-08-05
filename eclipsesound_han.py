#!/usr/bin/python3

"""
eclipsesound
~~~~~~~~~~~
Modified version of normalsound with fewer multi-frequency beams

:copyright: 2026 SuperDARN
:author: Evan Thomas
"""

import itertools
from utils.experiment_prototype import ExperimentPrototype
import borealis_experiments.superdarn_common_fields as scf


class EclipseSound(ExperimentPrototype):
    cpid = 1103

    def __init__(self):
        han_freq_bands = ([9051, 9129],     #0
                          [9911, 9984],     #1
                          [11086, 11164],   #2
                          [11561, 11589],   #3
                          [13451, 13499],   #4
                          [13881, 13889],   #5
                          [16221, 16369],   #6
                          [18041,18041],    #7
                          [19426, 19669],   #8
                          [19811, 19979])   #9

        sounding_beams = [3, 9]
        sounding_freqs = han_freq_bands[1:7]
        beam_nums = []
        freq_nums = []
        for b, f in itertools.product(sounding_beams, range(len(sounding_freqs))):
            beam_nums.append(b)
            freq_nums.append(f)

        common_intt_ms = 2000

        common_slice = {
                "pulse_sequence": scf.SEQUENCE_8P,
                "tau_spacing": scf.TAU_SPACING_8P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": common_intt_ms,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "tx_beam_order": scf.STD_BEAM_ORDER,
                "rx_beam_order": scf.STD_BEAM_ORDER,
                # this scanbound will be aligned because len(beam_order) = len(scanbound)
                "scanbound": scf.easy_scanbound(common_intt_ms, scf.STD_BEAM_ORDER),
                #"freq": scf.COMMON_MODE_FREQ_1,  # kHz
                "cfs_range": han_freq_bands[2],
                "acf": True,
                "xcf": True,  # cross-correlation processing
                "acfint": False,  # interferometer acfs
                "lag_table": scf.STD_8P_LAG_TABLE,  # lag table needed for 8P since not all lags used.
            }

        sounding_scanbound_spacing = 1.8  # seconds
        sounding_intt_ms = sounding_scanbound_spacing * 1.0e3 - 100

        # Starts at 32 s, after 16 beam slice finishes
        sounding_scanbound = [32 + i * sounding_scanbound_spacing for i in range(14)]

        sounding_slice = {
                "pulse_sequence": scf.SEQUENCE_8P,
                "tau_spacing": scf.TAU_SPACING_8P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": sounding_intt_ms,  # duration of an integration, in ms
                "beam_angle": scf.STD_BEAM_ANGLES,
                "tx_beam_order": beam_nums,
                "rx_beam_order": beam_nums,
                "scanbound": sounding_scanbound,
                "cfs_range": sounding_freqs,
                "freq_order": freq_nums,
                "acf": True,
                "xcf": True,  # cross-correlation processing
                "acfint": False,  # interferometer acfs
                "lag_table": scf.STD_8P_LAG_TABLE,  # lag table needed for 8P since not all lags used.
            }

        super().__init__(comment_string='August 2026 total solar eclipse experiment')

        self.add_slice(common_slice)
        self.add_slice(sounding_slice, {0: "SCAN"})
