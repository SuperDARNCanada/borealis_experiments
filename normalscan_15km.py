"""
normalscan_15km
~~~~~~~~~~~~~~~
Standard radar operating experiment with 15km resolution. Transmits a single frequency signal.

:copyright: 2025 SuperDARN Canada
"""

import borealis_experiments.superdarn_common_fields as scf
from utils import decimation_scheme as dm
from utils.experiment_prototype import ExperimentPrototype


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


class Normalscan15km(ExperimentPrototype):
    cpid = 3803

    def __init__(self, **kwargs):
        """
        kwargs:

        freq: int

        """
        super().__init__()

        self.add_slice(
            {  # slice_id = 0, there is only one slice.
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_15KM,
                "num_ranges": 225,
                "first_range": 90,
                "intt": scf.INTT_MS,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "rx_beam_order": scf.STD_BEAM_ORDER,
                "tx_beam_order": scf.STD_BEAM_ORDER,
                "scanbound": scf.STD_SCANBOUND,
                "freq": scf.COMMON_MODE_FREQ_1,  # kHz
                "acf": True,
                "xcf": True,  # cross-correlation processing
                "acfint": True,  # interferometer acfs
                "wait_for_first_scanbound": False,
                "decimation_scheme": filter_15km_mode(),
            }
        )
