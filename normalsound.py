#!/usr/bin/python3

"""
normalsound
~~~~~~~~~~~
Modified version of normalscan with added frequency sounding

:copyright: 2021 SuperDARN Canada
"""

import itertools
from experiment_prototype.experiment_prototype import ExperimentPrototype
import borealis_experiments.superdarn_common_fields as scf


class NormalSound(ExperimentPrototype):
    cpid = 157

    def __init__(self):
        sounding_beams = [0, 2, 4, 6, 8, 10, 12, 14, 1, 3, 5, 7, 9, 11, 13, 15]
        beam_nums = list()
        freq_nums = list()
        for b, f in itertools.product(sounding_beams, range(len(scf.SOUNDING_FREQS))):
            beam_nums.append(b)
            freq_nums.append(f)

        if scf.IS_FORWARD_RADAR:
            beams_to_use = scf.STD_16_FORWARD_BEAM_ORDER
        else:
            beams_to_use = scf.STD_16_REVERSE_BEAM_ORDER

        freqrange = (max(scf.SOUNDING_FREQS) - min(scf.SOUNDING_FREQS)) / 2
        centerfreq = min(scf.SOUNDING_FREQS) + freqrange

        slices = []

        common_scanbound_spacing = 3.0  # seconds
        common_intt_ms = (
            common_scanbound_spacing * 1.0e3 - 100
        )  # reduce by 100 ms for processing

        slices.append(
            {  # slice_id = 0, the first slice
                "pulse_sequence": scf.SEQUENCE_8P,
                "tau_spacing": scf.TAU_SPACING_8P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": common_intt_ms,  # duration of an integration, in ms
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "tx_beam_order": beams_to_use,
                "rx_beam_order": beams_to_use,
                # this scanbound will be aligned because len(beam_order) = len(scanbound)
                "scanbound": [
                    i * common_scanbound_spacing for i in range(len(beams_to_use))
                ],
                "freq": scf.COMMON_MODE_FREQ_1,  # kHz
                "txctrfreq": centerfreq,
                "rxctrfreq": centerfreq,
                "acf": True,
                "xcf": True,  # cross-correlation processing
                "acfint": True,  # interferometer acfs
                "lag_table": scf.STD_8P_LAG_TABLE,  # lag table needed for 8P since not all lags used.
            }
        )

        sounding_scanbound_spacing = 1.5  # seconds
        sounding_intt_ms = sounding_scanbound_spacing * 1.0e3 - 250

        sounding_scanbound = [48 + i * sounding_scanbound_spacing for i in range(8)]
        slices.append(
            {
                "pulse_sequence": scf.SEQUENCE_8P,
                "tau_spacing": scf.TAU_SPACING_8P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": sounding_intt_ms,  # duration of an integration, in ms
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "tx_beam_order": beam_nums,
                "rx_beam_order": beam_nums,
                "scanbound": sounding_scanbound,
                "freq": scf.SOUNDING_FREQS,
                "freq_order": freq_nums,
                "txctrfreq": centerfreq,
                "rxctrfreq": centerfreq,
                "acf": True,
                "xcf": True,  # cross-correlation processing
                "acfint": True,  # interferometer acfs
                "lag_table": scf.STD_8P_LAG_TABLE,  # lag table needed for 8P since not all lags used.
            }
        )

        super().__init__(comment_string=NormalSound.__doc__)

        self.add_slice(slices[0])
        self.add_slice(slices[1], {0: "SCAN"})
