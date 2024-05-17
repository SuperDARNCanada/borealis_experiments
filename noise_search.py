#!/usr/bin/python

"""
    noise_search.py
    ~~~~~~~~~~~~~~~~~~~~~~
    Runs through three frequencies. Each frequency does a normal averaging period, then runs transmits a single sequence
    while receiving at a high bandwidth, then listens for a single sequence while receiving at a high bandwidth.
    All slices are AVEPERIOD interfaced.

    :copyright: 2024 SuperDARN Canada
    :author: Remington Rohel
"""
import copy

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
from experiment_prototype.experiment_utils import decimation_scheme as decimation


def wideband_scheme():
    """
    Wide passband decimation scheme (high output sample rate, beware!)
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


class NoiseSearch(ExperimentPrototype):

    def __init__(self):
        cpid = 3386
        super().__init__(
            cpid,
            comment_string="Switches between three frequencies, each of which runs normally, then sends out two "
                           "sequences while receiving at a high bandwidth. The first sequence transmits, while the "
                           "second only receives.")

        if scf.IS_FORWARD_RADAR:
            beams_to_use = scf.STD_16_FORWARD_BEAM_ORDER
        else:
            beams_to_use = scf.STD_16_REVERSE_BEAM_ORDER

        slice_template = {  # slice_id = 0, added first
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": 3500,
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": beams_to_use,
            "tx_beam_order": beams_to_use,
            "acf": True,
            "xcf": True,
            "acfint": True,
        }

        interfacing_dict = None

        freqs = [scf.COMMON_MODE_FREQ_1, 12350, 12800]

        for freq in freqs:
            # Add a slice that transmits for each frequency
            default_slice = copy.deepcopy(slice_template)
            default_slice["freq"] = freq

            self.add_slice(default_slice, interfacing_dict=interfacing_dict)  # None for 1st slice
            interfacing_dict = {0: "AVEPERIOD"}  # All subsequent slices are AVEPERIOD interfaced with slice 0
            
            high_bandwidth_tx_slice = copy.deepcopy(default_slice)
            high_bandwidth_tx_slice["decimation_scheme"] = wideband_scheme()  # Use a high bandwidth filter scheme
            high_bandwidth_tx_slice.pop("intt")
            high_bandwidth_tx_slice["intn"] = 1  # Only run for 1 sequence
            high_bandwidth_tx_slice.pop("acf")
            high_bandwidth_tx_slice.pop("xcf")
            high_bandwidth_tx_slice.pop("acfint")
            self.add_slice(high_bandwidth_tx_slice, interfacing_dict=interfacing_dict)

            high_bandwidth_rx_slice = copy.deepcopy(high_bandwidth_tx_slice)
            high_bandwidth_rx_slice.pop("tx_beam_order")
            high_bandwidth_rx_slice["rxonly"] = True
            self.add_slice(high_bandwidth_rx_slice, interfacing_dict=interfacing_dict)
