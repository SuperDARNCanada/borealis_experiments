"""
rkn_noise_search
~~~~~~~~~~~~~~~~
Interleaved TX/RX experiment monitoring the interference/noise environment at RKN.

:copyright: 2025 SuperDARN Canada
"""

import copy

from experiment_prototype.experiment_prototype import ExperimentPrototype
import borealis_experiments.superdarn_common_fields as scf


class cfs_scan(ExperimentPrototype):
    cpid = 3497

    def __init__(self, **kwargs):
        if scf.IS_FORWARD_RADAR:
            beams_to_use = scf.STD_16_FORWARD_BEAM_ORDER
        else:
            beams_to_use = scf.STD_16_REVERSE_BEAM_ORDER

        slice_tx = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": beams_to_use,
            "tx_beam_order": beams_to_use,
            "scanbound": scf.easy_scanbound(scf.INTT_7P, beams_to_use),
            "cfs_range": [scf.COMMON_MODE_FREQ_1 - 150, scf.COMMON_MODE_FREQ_1 + 150],
            "cfs_always_run": True,
            "cfs_stable_time": 3600,  # 1 hour
            "acf": False,
            "comment": "TX mode",
        }

        slice_rx = copy.deepcopy(slice_tx)
        slice_rx.pop("tx_beam_order")
        slice_rx["rxonly"] = True
        slice_rx["comment"] = "RX mode"

        super().__init__(comment_string="Scanning noise environment in tx and rx modes")

        self.add_slice(slice_tx)
        self.add_slice(slice_rx, interfacing_dict={0: "AVEPERIOD"})
