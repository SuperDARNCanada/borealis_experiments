#!/usr/bin/python

"""
    eeaao
    ~~~~~~~~~~~~~
    The mode is a flexible multistatic multifrequency full FOV mode.
    Transmit and receive frequencies are configured via command line arguments.
    :copyright: 2023 SuperDARN Canada
    :author: Remington Rohel
"""
import copy

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
import experiment_prototype.experiment_utils.decimation_scheme as decimation


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


class EEAAO(ExperimentPrototype):
    """
    This experiment is configurable via arguments. The TX and RX frequencies in kHz must be specified by kwargs.
    All TX frequencies specified will also be used as RX frequencies, and at least one frequency must be specified as
    either an RX or TX frequency.
    """
    def __init__(self, **kwargs):
        """
        kwargs:
            tx_freqs: str, list of frequencies in kHz to transmit on. Format as "[10500,12000]" or "10500,12000"
            rx_freqs: str, list of frequencies in kHz to receive on. Format as "[10600,12200]" or "10600,12200"
        """
        cpid = 3777

        def parse_freqs_from_string(freqs):
            freq_list = []
            if freqs:
                for f in freqs.strip('[]').split(','):
                    freq_list.append(int(f))
            return freq_list

        tx_freqs = parse_freqs_from_string(kwargs.get('tx_freqs', ''))  # Default to no frequencies specified
        rx_freqs = parse_freqs_from_string(kwargs.get('rx_freqs', ''))  # Default to no frequencies specified

        all_freqs = set(tx_freqs).union(set(rx_freqs))
        if len(all_freqs) == 0:
            raise ValueError(f"No RX or TX frequencies specified.\t"
                             f"tx_freqs: {kwargs.get('tx_freqs', '')}\t"
                             f"rx_freqs: {kwargs.get('rx_freqs', '')}")

        if len(set(tx_freqs)) != len(tx_freqs):
            raise ValueError(f"Duplicate TX frequencies specified: {tx_freqs}")
        if len(set(rx_freqs)) != len(rx_freqs):
            raise ValueError(f"Duplicate RX frequencies specified: {rx_freqs}")

        # Calculate center frequency
        max_freq = max(all_freqs)
        min_freq = min(all_freqs)
        center_freq = (max_freq + min_freq) / 2.0   # Center frequency set to middle of the range

        comment_string = f"TX freqs: {tx_freqs}, RX freqs: {rx_freqs}"

        super().__init__(cpid, txctrfreq=center_freq, rxctrfreq=center_freq, comment_string=comment_string)

        default_slice = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,  # duration of an integration, in ms
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": [scf.STD_16_FORWARD_BEAM_ORDER],   # All beams
            "scanbound": [i * 3.7 for i in range(len(scf.STD_16_BEAM_ANGLE))],  # align each aveperiod to 3.7s boundary
            "wait_for_first_scanbound": False,
            "align_sequences": True,     # align start of sequence to tenths of a second
        }

        num_antennas = scf.options.main_antenna_count
        left_half_antennas = [i for i in range(num_antennas // 2)]
        right_half_antennas = [i for i in range(num_antennas // 2, num_antennas)]
        all_antennas = [i for i in range(num_antennas)]

        all_slices = []
        for i, freq in enumerate(tx_freqs):
            new_slice = copy.deepcopy(default_slice)
            new_slice['freq'] = freq
            new_slice['tx_antenna_pattern'] = scf.easy_widebeam
            if len(tx_freqs) == 2:  # Use 8-antenna wide-beam mode if only transmitting on two frequencies
                if i == 0:
                    new_slice['tx_antennas'] = left_half_antennas
                else:
                    new_slice['tx_antennas'] = right_half_antennas
            else:   # Use 16-antenna wide-beam mode otherwise
                new_slice['tx_antennas'] = all_antennas
            new_slice['tx_beam_order'] = [0]
            new_slice['comment'] = f"TX slice with frequency {freq}"
            all_slices.append(new_slice)

        # Add the slices to the experiment
        for freq in rx_freqs:
            if freq in tx_freqs:    # Already listening on this frequency, skip
                continue
            new_slice = copy.deepcopy(default_slice)
            new_slice['freq'] = freq
            new_slice['rxonly'] = True
            new_slice['comment'] = f"RX slice with frequency {freq}"
            all_slices.append(new_slice)

        self.add_slice(all_slices[0])
        for this_slice in all_slices[1:]:
            self.add_slice(this_slice, {0: 'CONCURRENT'})