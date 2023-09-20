#!/usr/bin/python

"""
    normalscan_ppo_test
    ~~~~~~~~~~~~~~~~~~~
    normalscan but pulse phase offset is modified

    :copyright: 2022 SuperDARN Canada
"""

import numpy as np

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
from experiment_prototype.experiment_utils.decimation_scheme import \
    DecimationScheme, DecimationStage, create_firwin_filter_by_attenuation


def create_single_stage_scheme():
    """
    Frankenstein script by Devin Huyghebaert for 15 km range gates with
    a special ICEBEAR collab mode

    Built off of the default scheme used for 45 km with minor changes.

    :return DecimationScheme: a decimation scheme for use in experiment.
    """

    rates = [5.0e6]  # last stage 100.0e3
    dm_rates = [50]
    transition_widths = [50.0e3]
    cutoffs = [100.0e3]
    ripple_dbs = [100.0]
    scaling_factors = [100.0]
    all_stages = []

    for stage in range(0, len(rates)):
        filter_taps = list(
            scaling_factors[stage] * create_firwin_filter_by_attenuation(
                rates[stage], transition_widths[stage], cutoffs[stage],
                ripple_dbs[stage]))
        all_stages.append(DecimationStage(stage, rates[stage],
                          dm_rates[stage], filter_taps))

    return DecimationScheme(rates[0], rates[-1]/dm_rates[-1], stages=all_stages)


def pulse_encode(beam_iter, sequence_num, num_pulses):
    codes = np.ones((num_pulses, 30), dtype=np.complex64)        # Each pulse is 30 chips long
    codes[:, :] = np.array([-1, -1, -1, -1, 1, 1, 1, 1, 1, 1, -1, 1, 1, -1, 1, 1, -1, 1, -1, 1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1], dtype=np.complex64)
    codes[1::2, :] *= -1.0
    return codes


class NormalscanPulseCodesTest(ExperimentPrototype):

    def __init__(self, **kwargs):
        """
        kwargs:

        freq: int

        """
        cpid = 10052
        super().__init__(cpid)

        beams_to_use = scf.STD_16_FORWARD_BEAM_ORDER
        num_ranges = scf.STD_NUM_RANGES
        decimation_scheme = create_single_stage_scheme()
        # default frequency set here
        freq = scf.COMMON_MODE_FREQ_1
        
        if kwargs:
            if 'freq' in kwargs.keys():
                freq = kwargs['freq']
        
        print('Frequency set to {}'.format(freq))   # TODO: Log

        self.add_slice({    # slice_id = 0, there is only one slice.
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": num_ranges,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,    # duration of an integration, in ms
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "tx_beam_order": beams_to_use,
            "rx_beam_order": beams_to_use,
            "freq": freq,       # kHz
            "acf": False,
            "xcf": False,       # cross-correlation processing
            "acfint": False,    # interferometer acfs
            "pulse_codes": pulse_encode,
            "decimation_scheme": decimation_scheme
        })

