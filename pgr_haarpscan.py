"""
pgr_haarpscan
~~~~~~~~~~~~~
Uses 2 beams westward (CCW w.r.t. boresight) of the PGR FOV to focus on the ionosphere in the direction
of the HAARP instrument in Alaska.

:copyright: 2025 SuperDARN Canada
"""

import copy
import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
import utils.decimation_scheme as dm


def filter_15km_mode():
    sample_rate = 5e6  # 5 MHz
    dm_rate = [25, 20]  # downsampling rates after filters
    transition_width = [150e3, 30e3]  # transition from passband to stopband
    cutoff_hz = [10e3, 5e3]  # bandwidth for output of filter
    ripple_db = [115, 50]  # dB between passband and stopband
    scaling_factors = [1000.0, 10000.0]  # multiplicative factors for each filter stage

    dm_rate_so_far = 1
    stages = []

    # First stage Kaiser
    taps = scaling_factors[0] * dm.create_firwin_filter_by_attenuation(
        sample_rate, transition_width[0], cutoff_hz[0], ripple_db[0]
    )
    stages.append(dm.DecimationStage(0, sample_rate, dm_rate[0], taps.tolist()))
    dm_rate_so_far *= dm_rate[0]

    # Second stage Kaiser by num taps
    taps = scaling_factors[1] * dm.create_firwin_filter_by_num_taps(
        sample_rate / dm_rate_so_far, cutoff_hz[1], 41
    )
    stages.append(
        dm.DecimationStage(1, sample_rate / dm_rate_so_far, dm_rate[1], taps.tolist())
    )
    dm_rate_so_far *= dm_rate[1]

    scheme = dm.DecimationScheme(
        sample_rate, sample_rate / dm_rate_so_far, stages=stages
    )

    return scheme


class PgrHaarpscan(ExperimentPrototype):
    cpid = 3498

    def __init__(self, **kwargs):
        super().__init__(
            comment_string="Scan of beams extra westward beams at PGR, overlooking HAARP."
        )

        slice_0 = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_15KM,
            "num_ranges": 225,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,
            "beam_angle": [
                scf.STD_16_BEAM_ANGLE[0] - (3.24 * 3),
                scf.STD_16_BEAM_ANGLE[0] - (3.24 * 2),
            ],  # 2 beams CCW of FOV, essentially beams -3 and -2
            "rx_beam_order": [0, 1],
            "tx_beam_order": [0, 1],
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
            "xcf": True,
            "acfint": False,
            "decimation_scheme": filter_15km_mode(),
        }
        slice_1 = copy.deepcopy(slice_0)
        slice_1["freq"] = scf.COMMON_MODE_FREQ_2

        self.add_slice(slice_0)
        self.add_slice(slice_1, interfacing_dict={0: "SCAN"})
