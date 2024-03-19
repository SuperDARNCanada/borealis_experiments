#!/usr/bin/python

"""
dm_test
~~~~~~~~~~
Tests a new DecimationScheme by AvePeriod interfacing with the default DecimationScheme.

:copyright: 2024 SuperDARN Canada
"""
import copy

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
import experiment_prototype.experiment_utils.decimation_scheme as decimation


class DmTest(ExperimentPrototype):

    def __init__(self, **kwargs):
        """
        kwargs:

        freq: int

        """
        cpid = 3805
        super().__init__(cpid)

        if scf.IS_FORWARD_RADAR:
            beams_to_use = scf.STD_16_FORWARD_BEAM_ORDER
        else:
            beams_to_use = scf.STD_16_REVERSE_BEAM_ORDER

        if scf.options.site_id in ["cly", "rkn", "inv"]:
            num_ranges = scf.POLARDARN_NUM_RANGES
        if scf.options.site_id in ["sas", "pgr", "lab"]:
            num_ranges = scf.STD_NUM_RANGES

        # default frequency set here
        freq = scf.COMMON_MODE_FREQ_1

        if kwargs:
            if 'freq' in kwargs.keys():
                freq = kwargs['freq']

        print('Frequency set to {}'.format(freq))   # TODO: Log

        slice_0 = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": num_ranges,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,  # duration of an integration, in ms
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": beams_to_use,
            "tx_beam_order": beams_to_use,
            "freq" : freq, #kHz
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
            "wait_for_first_scanbound": False,
        }
        slice_1 = copy.deepcopy(slice_0)
        slice_1['decimation_scheme'] = two_stage_flatpass_v2()

        self.add_slice(slice_0)
        self.add_slice(slice_1, {0: 'AVEPERIOD'})


def two_stage_flatpass_v2():
    """
    Two-stage kaiser window scheme.

    Works well with the following parameters:
    sample_rate = 5e6
    dm_rate = [50, 30]
    transition_width = [150e3, 25e3]
    cutoff_hz = [10e3, 5e3]
    ripple_db = [115, 50]
    """
    sample_rate = 5e6                    # 5 MHz
    dm_rate = [50, 30]                   # downsampling rates after filters
    transition_width = [150e3, 30e3]     # transition from passband to stopband
    cutoff_hz = [10e3, 5e3]              # bandwidth for output of filter
    ripple_db = [115, 50]                # dB between passband and stopband

    dm_rate_so_far = 1
    stages = []
    for i in range(2):
        rate = sample_rate / dm_rate_so_far
        taps = decimation.create_firwin_filter_by_attenuation(rate,
                                                              transition_width[i],
                                                              cutoff_hz[i],
                                                              ripple_db[i])
        stages.append(decimation.DecimationStage(i, rate, dm_rate[i], taps.tolist()))
        dm_rate_so_far *= dm_rate[i]

    scheme = decimation.DecimationScheme(sample_rate, sample_rate / dm_rate_so_far, stages=stages)

    return scheme


