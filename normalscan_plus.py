"""
normalscan_plus
~~~~~~~~~~
Standard radar operating experiment, plus an extra concurrent listening frequency.
Transmits a single frequency signal.

:copyright: 2023 SuperDARN Canada
"""

import copy
import borealis_experiments.superdarn_common_fields as scf
from utils.experiment_prototype import ExperimentPrototype


class NormalscanPlus(ExperimentPrototype):
    cpid = 3815

    def __init__(self, **kwargs):
        """
        kwargs:

        freq: int

        """
        super().__init__(comment_string="Normalscan with extra concurrent listening")

        # default frequency set here
        freq = kwargs.get("freq", scf.COMMON_MODE_FREQ_1)

        self.add_slice(
            {  # slice_id = 0, there is only one slice.
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
                "freq": freq,  # kHz
                "acf": True,
                "xcf": True,  # cross-correlation processing
                "acfint": True,  # interferometer acfs
                "wait_for_first_scanbound": False,
                "comment": "Standard normalscan slice",
            }
        )

        if "listening_freqs" in kwargs:
            slice_template = {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": scf.INTT_MS,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "rx_beam_order": scf.STD_BEAM_ORDER,
                "rxonly": True,
                "scanbound": scf.STD_SCANBOUND,
                "acf": False,
                "wait_for_first_scanbound": False,
                "comment": "Listening-only slice, concurrent with transmitting normalscan slice",
            }

            listening_freqs = [int(x) for x in kwargs.get("listening_freqs").split(",")]
            for freq in listening_freqs:
                new_slice = copy.deepcopy(slice_template)
                new_slice["freq"] = freq
                self.add_slice(new_slice, interfacing_dict={0: "CONCURRENT"})
