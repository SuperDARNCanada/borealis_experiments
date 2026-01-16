#!/usr/bin/python3

"""
themisscan
~~~~~~~~~~
notes on ThemisScan purpose here TODO

last scheduled 2019-12-29

:copyright: 2019 SuperDARN Canada
"""

from utils.experiment_prototype import ExperimentPrototype
import borealis_experiments.superdarn_common_fields as scf


class ThemisScan(ExperimentPrototype):
    cpid = 3300

    def __init__(
        self,
    ):
        forward_beams = [
            0,
            "camp",
            1,
            "camp",
            2,
            "camp",
            3,
            "camp",
            4,
            "camp",
            5,
            "camp",
            6,
            "camp",
            7,
            "camp",
            8,
            "camp",
            9,
            "camp",
            10,
            "camp",
            11,
            "camp",
            12,
            "camp",
            13,
            "camp",
            14,
            "camp",
            15,
            "camp",
            "camp",
            "camp",
            "camp",
            "camp",
            "camp",
            "camp",
        ]
        reverse_beams = [
            15,
            "camp",
            14,
            "camp",
            13,
            "camp",
            12,
            "camp",
            11,
            "camp",
            10,
            "camp",
            9,
            "camp",
            8,
            "camp",
            7,
            "camp",
            6,
            "camp",
            5,
            "camp",
            4,
            "camp",
            3,
            "camp",
            2,
            "camp",
            1,
            "camp",
            0,
            "camp",
            "camp",
            "camp",
            "camp",
            "camp",
            "camp",
            "camp",
        ]

        if scf.config.scan_direction == "forward":
            beams_to_use = forward_beams
        else:
            beams_to_use = reverse_beams

        if scf.config.site_id in ["sas", "inv", "cly"]:
            camp = 6
        elif scf.config.site_id in ["pgr"]:
            camp = 12
        elif scf.config.site_id in ["rkn"]:
            camp = 7
        else:
            camp = 8

        if scf.config.site_id in ["sas", "pgr", "cly"]:
            freq = 10500
        elif scf.config.site_id in ["rkn"]:
            freq = 12200
        elif scf.config.site_id in ["inv"]:
            freq = 12100
        else:
            freq = 12400

        beams_to_use = [camp if bm == "camp" else bm for bm in beams_to_use]

        slice_1 = {  # slice_id = 0, the first slice
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": 2900,  # duration of an integration, in ms
            "beam_angle": scf.STD_BEAM_ANGLES,
            "rx_beam_order": beams_to_use,
            "tx_beam_order": beams_to_use,
            "scanbound": scf.easy_scanbound(3000, beams_to_use),
            "freq": freq,  # kHz
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
        }
        super().__init__()

        self.add_slice(slice_1)
