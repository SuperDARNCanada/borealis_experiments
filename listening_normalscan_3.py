#!/usr/bin/python

"""
    listening_normalscan_3
    ~~~~~~~~~~
    Standard radar operating experiment, with an additional listening period at the end of each integration time.
    Transmits a single frequency signal.

    :copyright: 2024 SuperDARN Canada
"""
import copy

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
import experiment_prototype.experiment_utils.decimation_scheme as decimation


def clrfrq_scheme():
    """
    Wide passband decimation scheme for listening only (high output sample rate, beware!)
    """
    sample_rate = 5e6           # 5 MHz
    dm_rate = [15]              # downsampling rates after filters
    transition_width = [100e3]  # transition from passband to stopband
    cutoff_hz = [165e3]         # bandwidth for output of filter
    ripple_db = [200]           # Stopband suppression in dB

    dm_rate_so_far = 1
    stages = []
    for i in range(len(ripple_db)):
        rate = sample_rate / dm_rate_so_far
        taps = decimation.create_firwin_filter_by_attenuation(rate,
                                                              transition_width[i],
                                                              cutoff_hz[i],
                                                              ripple_db[i])
        stages.append(decimation.DecimationStage(i, rate, dm_rate[i], taps.tolist()))
        dm_rate_so_far *= dm_rate[i]

    scheme = decimation.DecimationScheme(sample_rate, sample_rate / dm_rate_so_far, stages=stages)

    return scheme


class ListeningNormalscan3(ExperimentPrototype):

    def __init__(self, **kwargs):
        """
        kwargs:

        freq: int

        """
        cpid = 3385
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

        slice_0 = {  # slice_id = 0, there is only one slice.
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

        # This slice does not transmit, and only collects one sequence.
        slice_1 = copy.deepcopy(slice_0)
        del slice_1['tx_beam_order']
        del slice_1['intt']
        slice_1['intn'] = 1
        slice_1['acf'] = False
        slice_1['xcf'] = False
        slice_1['acfint'] = False
        slice_1['decimation_scheme'] = clrfrq_scheme()
        slice_1['rxonly'] = True

        self.add_slice(slice_0)
        self.add_slice(slice_1, {0: 'AVEPERIOD'})

