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


class EEAAO(ExperimentPrototype):
    """
    This experiment is configurable via arguments. The TX and RX frequencies in kHz must be specified by kwargs.
    All TX frequencies specified will also be used as RX frequencies, and at least one frequency must be specified as
    either an RX or TX frequency.
    """
    def __init__(self, **kwargs):
        """
        kwargs:
            tx_freqs: str, frequencies in kHz to transmit on. E.g. "10500,12000"
            rx_freqs: str, frequencies in kHz to receive on. E.g. "10500,12000"
        """
        cpid = 3777

        num_ranges = scf.STD_NUM_RANGES

        def parse_freqs_from_string(freqs):
            freq_list = []
            for freq in freqs.split(','):
                freq_list.append(int(freq))
            return freq_list

        tx_freqs = parse_freqs_from_string(kwargs.get('tx_freqs', ''))  # Default to no frequencies specified
        rx_freqs = parse_freqs_from_string(kwargs.get('rx_freqs', ''))  # Default to no frequencies specified

        if len(set(tx_freqs)) != len(kwargs.get('tx_freqs', '').split(',')):
            raise ValueError(f"Duplicate TX frequencies specified: {kwargs.get('tx_freqs', '')}")
        if len(set(rx_freqs)) != len(kwargs.get('rx_freqs', '').split(',')):
            raise ValueError(f"Duplicate RX frequencies specified: {kwargs.get('rx_freqs', '')}")

        all_freqs = set(tx_freqs).union(set(rx_freqs))
        if len(all_freqs) == 0:
            raise ValueError("No RX or TX frequencies specified")

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
            "num_ranges": num_ranges,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,  # duration of an integration, in ms
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": [[i for i in range(scf.STD_16_BEAM_ANGLE)]],   # All beams
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
