#!/usr/bin/python

"""
    full_fov
    ~~~~~~~~
    The mode transmits with a pre-calculated phase progression across the array which illuminates
    the full FOV, and receives on all antennas. The first pulse in each sequence starts on the 0.1
    second boundaries, to enable bistatic listening on other radars.

    :copyright: 2022 SuperDARN Canada
    :author: Remington Rohel
"""

import numpy as np
from experiment_prototype.experiment_utils.sample_building import get_phase_shift

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype


def rx_phase_pattern(beam_angle, freq_khz, antenna_count, antenna_spacing, offset=0.0):
    window = [0.08081232549588463, 0.12098514265395757, 0.23455777475180511, 0.4018918165398586,
              0.594054435182454, 0.7778186328978896, 0.9214100134552521, 1.0,
              1.0, 0.9214100134552521, 0.7778186328978896, 0.594054435182454,
              0.4018918165398586, 0.23455777475180511, 0.12098514265395757, 0.08081232549588463]

    xcf_directions = {
        10400: [-28.8, -23.96, -19.92, -14.68, -11.24, -7.4, -3.48, -1.36,
                1.36, 3.48, 7.5, 11.24, 14.68, 19.92, 23.96, 28.8],
        10500: [-28.8, -23.86, -20.02, -14.78, -11.24, -7.5, -3.53, -1.41,
                1.41, 3.53, 7.5, 11.24, 14.78, 20.02, 23.86, 29.],
        10600: [-29., -23.76, -20.02, -14.78, -11.24, -7.5, -3.48, -1.32,
                1.32, 3.48, 7.6, 11.24, 14.78, 20.02, 23.76, 29.],
        10700: [-29.1, -23.76, -20.12, -14.88, -11.24, -7.6, -3.53, -1.32,
                1.32, 3.53, 7.6, 11.24, 14.88, 20.12, 23.76, 29.2],
        10800: [-29.3, -23.76, -20.12, -14.98, -11.24, -7.6, -3.53, -1.32,
                1.32, 3.53, 7.7, 11.24, 14.98, 20.12, 23.76, 29.4],
        10900: [-29.3, -23.66, -20.12, -15.08, -11.24, -7.7, -3.56, -1.32,
                1.32, 3.56, 7.7, 11.24, 15.08, 20.12, 23.66, 29.4],
        12200: [-28.4, -22.26, -17.62, -14.78, -11.24, -8.15, -4.96, -1.82,
                1.82, 4.96, 8.15, 11.24, 14.78, 17.62, 22.26, 28.5],
        12300: [-28.5, -22.46, -17.62, -14.78, -11.24, -8.1, -4.96, -1.82,
                1.82, 4.96, 8.1, 11.24, 14.78, 17.62, 22.46, 28.6],
        12500: [-28.7, -22.56, -17.62, -14.69, -11.24, -7.9, -4.88, -1.92,
                1.92, 4.88, 7.9, 11.24, 14.69, 17.62, 22.56, 28.8],
        13000: [-29.3, -22.86, -17.72, -14.58, -11.14, -7.6, -4.96, -2.12,
                2.12, 4.96, 7.6, 11.14, 14.58, 17.72, 22.86, 29.4],
        13100: [-29.6, -22.96, -17.82, -14.48, -11.34, -7.55, -4.93, -2.12,
                2.12, 4.93, 7.55, 11.34, 14.48, 17.82, 22.96, 29.7],
        13200: [-29.6, -23.06, -17.92, -14.48, -11.24, -7.6, -4.96, -2.12,
                2.12, 4.96, 7.6, 11.24, 14.48, 17.92, 23.06, 29.7],
        }

    shift = get_phase_shift(xcf_directions[int(freq_khz)], freq_khz, antenna_count,
                            antenna_spacing, offset) * 0.9999999

    # Apply a Hamming window to the antenna data streams of the main array
    if antenna_count == 16:
        shift = np.einsum('ij,j->ij', shift, np.array(window, dtype=np.float32))

    return shift


class FullFOV(ExperimentPrototype):
    def __init__(self, **kwargs):
        """
        kwargs:

        freq: int

        """
        cpid = 3800
        super().__init__(cpid)

        num_ranges = scf.STD_NUM_RANGES
        if scf.options.site_id in ["cly", "rkn", "inv"]:
            num_ranges = scf.POLARDARN_NUM_RANGES

        # default frequency set here
        freq = scf.COMMON_MODE_FREQ_1

        if kwargs:
            if 'freq' in kwargs.keys():
                freq = kwargs['freq']

        print('Frequency set to {}'.format(freq))   # TODO: Log

        num_antennas = scf.options.main_antenna_count

        self.add_slice({  # slice_id = 0, there is only one slice.
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": num_ranges,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,  # duration of an integration, in ms
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": [[i for i in range(num_antennas)]],
            "tx_beam_order": [0],   # only one pattern
            "tx_antenna_pattern": scf.easy_widebeam,
            "rx_antenna_pattern": rx_phase_pattern,
            "freq": freq,  # kHz
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
            #"align_sequences": True,     # align start of sequence to tenths of a second
        })
