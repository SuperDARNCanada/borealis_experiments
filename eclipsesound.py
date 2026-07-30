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
        sounding_beams = [0, 7]
        sounding_freqs = scf.SOUNDING_FREQS[:7]
        beam_nums = list()
        freq_nums = list()
        for b, f in itertools.product(sounding_beams, range(len(sounding_freqs))):
            beam_nums.append(b)
            freq_nums.append(f)

        slices = []

        common_intt_ms = 2000   # Shortened from typical 3000 ms. Will 16 beam slice at 32 s

        slices.append(
            {  # slice_id = 0, the first slice
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
                "freq": scf.COMMON_MODE_FREQ_1,  # kHz
                "acf": True,
                "xcf": True,  # cross-correlation processing
                "acfint": False,  # interferometer acfs
                "lag_table": scf.STD_8P_LAG_TABLE,  # lag table needed for 8P since not all lags used.
            }
        )

        sounding_scanbound_spacing = 1.8  # seconds
        sounding_intt_ms = sounding_scanbound_spacing * 1.0e3 - 100

        # Starts at 32 s, after 16 beam slice finishes
        sounding_scanbound = [32 + i * sounding_scanbound_spacing for i in range(14)]
        slices.append(
            {
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
                "freq": sounding_freqs,
                "freq_order": freq_nums,
                "acf": True,
                "xcf": True,  # cross-correlation processing
                "acfint": False,  # interferometer acfs
                "lag_table": scf.STD_8P_LAG_TABLE,  # lag table needed for 8P since not all lags used.
            }
        )

        super().__init__(comment_string="August 2026 total solar eclipse experiment")

        self.add_slice(slices[0])
        self.add_slice(slices[1], {0: "SCAN"})
