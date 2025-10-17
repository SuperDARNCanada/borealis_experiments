#!/usr/bin/python
"""
full_fov_15km
~~~~~~~~~~~~~
The mode transmits with a pre-calculated phase progression across the array which illuminates
the full FOV, and receives on all antennas. This mode uses 15-km range gates for high spatial resolution.

:copyright: 2022 SuperDARN Canada
:author: Remington Rohel
"""

import borealis_experiments.superdarn_common_fields as scf
from utils.experiment_prototype import ExperimentPrototype
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


class FullFOV15Km(ExperimentPrototype):
    cpid = 3801

    def __init__(self, **kwargs):
        """
        The mode transmits with a pre-calculated phase progression across the array which illuminates
        the full FOV, and receives on all antennas. This mode uses 15-km range gates for high spatial resolution.
        """
        super().__init__(comment_string="Full FOV 15km Resolution Experiment")

        self.add_slice(
            {  # slice_id = 0, there is only one slice.
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_15KM,
                "num_ranges": scf.STD_NUM_RANGES
                * 3,  # Each range is a third of the usual size, want same spatial extent
                "first_range": 90,  # km from radar
                "intt": scf.INTT_7P,  # duration of an integration, in ms
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "rx_beam_order": [[i for i in range(len(scf.STD_16_BEAM_ANGLE))]],
                "tx_beam_order": [0],  # only one pattern
                "tx_antenna_pattern": scf.easy_widebeam,
                "freq": scf.COMMON_MODE_FREQ_1,  # kHz
                "decimation_scheme": filter_15km_mode(),
                "acf": True,
                "xcf": True,
            }
        )
