#!/usr/bin/python3

"""
eclipsesound
~~~~~~~~~~~
Modified version of normalsound with fewer multi-frequency beams

:copyright: 2026 SuperDARN
:author: Evan Thomas
"""

from experiment_prototype.experiment_prototype import ExperimentPrototype
import borealis_experiments.superdarn_common_fields as scf


class EclipseSound(ExperimentPrototype):
    cpid = 1103

    def __init__(self):
        SOUNDING_BEAMS = {
            "cly": [0, 15],
            "inv": [0, 10],
            "pgr": [7, 15],
            "rkn": [2, 15],
            "sas": [2, 15],
        }

        sounding_beams = SOUNDING_BEAMS.get(scf.options.site_id)

        if scf.IS_FORWARD_RADAR:
            beam_order = scf.STD_16_FORWARD_BEAM_ORDER
        else:
            beam_order = scf.STD_16_REVERSE_BEAM_ORDER

        slices = []

        common_intt_ms = 2000

        slices.append(
            {  # slice_id = 0, the first slice
                "pulse_sequence": scf.SEQUENCE_8P,
                "tau_spacing": scf.TAU_SPACING_8P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": common_intt_ms,
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "tx_beam_order": beam_order,
                "rx_beam_order": beam_order,
                # this scanbound will be aligned because len(beam_order) = len(scanbound)
                "scanbound": scf.easy_scanbound(common_intt_ms, beam_order),
                "freq": scf.COMMON_MODE_FREQ_1,  # kHz
                "acf": True,
                "xcf": True,  # cross-correlation processing
                "acfint": False,  # interferometer acfs
                "lag_table": scf.STD_8P_LAG_TABLE,  # lag table needed for 8P since not all lags used.
            }
        )

        sounding_scanbound_spacing = 1.8  # seconds
        sounding_intt_ms = sounding_scanbound_spacing * 1.0e3 - 100

        sounding_scanbound = [32 + i * sounding_scanbound_spacing for i in range(14)]
        for freq in scf.SOUNDING_FREQS[:7]:
            slices.append(
                {
                    "pulse_sequence": scf.SEQUENCE_8P,
                    "tau_spacing": scf.TAU_SPACING_8P,
                    "pulse_len": scf.PULSE_LEN_45KM,
                    "num_ranges": scf.STD_NUM_RANGES,
                    "first_range": scf.STD_FIRST_RANGE,
                    "intt": sounding_intt_ms,  # duration of an integration, in ms
                    "beam_angle": scf.STD_16_BEAM_ANGLE,
                    "tx_beam_order": sounding_beams,
                    "rx_beam_order": sounding_beams,
                    "scanbound": sounding_scanbound,
                    "freq": freq,
                    "acf": True,
                    "xcf": True,  # cross-correlation processing
                    "acfint": False,  # interferometer acfs
                    "lag_table": scf.STD_8P_LAG_TABLE,  # lag table needed for 8P since not all lags used.
                }
            )

        super().__init__(self.cpid, comment_string='August 2026 total solar eclipse experiment')

        self.add_slice(slices[0])
        self.add_slice(slices[1], {0: 'SCAN'})
        for slice_num in range(2, len(slices)):
            self.add_slice(slices[slice_num], {1: 'AVEPERIOD'})