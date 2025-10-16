#!/usr/bin/python

"""
full_fov_twofsound
~~~~~~~~~~~~~~~~~~
The mode transmits with a pre-calculated phase progression across the array which illuminates
the full FOV, and receives on all antennas. Two frequencies are used, switching every integration time.

:copyright: 2025 SuperDARN Canada
:author: Remington Rohel
"""
import copy

import numpy as np

from utils.signals import get_phase_shift
import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype


def rx_phase_pattern(beam_angle, freq_khz, antenna_locations):
    # Chebyshev 30-dB window
    window = [0.2910, 0.3173, 0.4557, 0.6018, 0.7424, 0.8637, 0.9528, 1.0000,
              1.0000, 0.9528, 0.8637, 0.7424, 0.6018, 0.4557, 0.3173, 0.2910]

    adjusted_rx_beam_directions = {
        10400: [-25., -21.2, -18.3, -15.5, -11.4, -7.7, -5., -2.1,
                2.1, 5., 7.7, 11.4, 15.5, 18.3, 21.2, 25.],
        10500: [-24.8, -20.7, -17.9, -14.8, -11.8, -8.6, -4.9, -1.9,
                1.9, 4.9, 8.6, 11.8, 14.8, 17.9, 20.7, 24.8],
        10600: [-25., -20.7, -17.8, -14.9, -11.9, -8.5, -4.8, -1.9,
                1.9, 4.8, 8.5, 11.9, 14.9, 17.8, 20.7, 25.],
        10700: [-24.5, -21.4, -18.1, -15.3, -11.5, -7.7, -5.1, -2.1,
                2.1, 5.1, 7.7, 11.5, 15.3, 18.1, 21.4, 24.5],
        10800: [-25., -20.9, -17.8, -15.3, -11.6, -7.8, -4.8, -2.1,
                2.1, 4.8, 7.8, 11.6, 15.3, 17.8, 20.9, 25.],
        10900: [-24.9, -20.9, -17.7, -15.3, -11.7, -7.8, -4.7, -2.,
                2., 4.7, 7.8, 11.7, 15.3, 17.7, 20.9, 25.],
        12200: [-24.4, -21.5, -17.7, -14.2, -11.5, -8.2, -4.8, -1.8,
                1.8, 4.8, 8.2, 11.5, 14.2, 17.7, 21.5, 24.4],
        12300: [-24.2, -21.5, -17.5, -14.4, -11.5, -7.9, -5., -2.1,
                2.1, 5., 7.9, 11.5, 14.4, 17.5, 21.5, 24.2],
        12500: [-24.3, -21.4, -17.8, -14.1, -11.4, -8.2, -4.9, -1.8,
                1.8, 4.9, 8.2, 11.4, 14.1, 17.8, 21.4, 24.3],
        13000: [-23.9, -21.5, -18.4, -14.8, -11.4, -7.8, -4.6, -2.4,
                2.4, 4.6, 7.8, 11.4, 14.8, 18.4, 21.5, 23.9],
        13100: [-24.5, -21., -18.4, -13.7, -11.1, -8.5, -4.7, -1.5,
                1.5, 4.7, 8.5, 11.1, 13.7, 18.4, 21., 24.5],
        13200: [-24.8, -21.6, -18.4, -14., -11.7, -8.4, -4.6, -2.2,
                2.2, 4.6, 8.4, 11.7, 14., 18.4, 21.6, 24.8],
    }

    shift = get_phase_shift(adjusted_rx_beam_directions[int(freq_khz)], [freq_khz], antenna_locations[:, 0])[0] * 0.9999999
    # shift: [16, 16]  (i.e. [num_beams, num_tx_channels])

    # Apply a window to the antenna data streams of the main array
    if antenna_locations.shape[0] == 16:
        shift = np.einsum('ij,j->ij', shift, np.array(window, dtype=np.float32))

    return shift


class FullFOVTwoFSound(ExperimentPrototype):
    cpid = 3809

    def __init__(self, **kwargs):
        """
        Supported kwargs:
        freq1: int, frequency of first slice, in kHz.
        freq2: int, frequency of second slice, in kHz.
        """
        super().__init__()

        freq1 = kwargs.get("freq1", scf.COMMON_MODE_FREQ_1)
        freq2 = kwargs.get("freq2", scf.COMMON_MODE_FREQ_2)

        slice_0 = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,  # duration of an integration, in ms
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": [[i for i in range(len(scf.STD_16_BEAM_ANGLE))]],
            "tx_beam_order": [0],   # only one pattern
            "tx_antenna_pattern": scf.easy_widebeam,
            "rx_antenna_pattern": rx_phase_pattern,
            "freq": freq1,  # kHz
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": False,  # interferometer acfs
        }

        slice_1 = copy.deepcopy(slice_0)
        slice_1['freq'] = freq2

        self.add_slice(slice_0)
        self.add_slice(slice_1, interfacing_dict={0: "SCAN"})
