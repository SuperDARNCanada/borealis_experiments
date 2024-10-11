#!/usr/bin/python

"""
    full_fov_60deg
    ~~~~~~~~~~~~~~
    The mode transmits with a pre-calculated phase progression across the array which illuminates
    a 60-degree FOV, and receives on all antennas.

    :copyright: 2024 SuperDARN Canada
    :author: Remington Rohel
"""
import copy

import numpy as np

from utils.signals import get_phase_shift
import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype

def sixty_deg_widebeam(frequency_khz, tx_antennas, antenna_spacing_m):
    """
    Returns phases in degrees for each antenna in the main array that will generate a wide beam pattern
    that illuminates a 60-degree FOV. Only 16 antennas at common frequencies is supported.
    """
    if antenna_spacing_m != 15.24:
        raise ValueError(f"Antenna spacing must be 15.24m. Given value: {antenna_spacing_m}")

    cached_values_16_antennas = {
        10400: [0., 96.46449659, 157.09170077, 233.12839748, 307.31676976, 357.77417584, 380.30223006, 358.50566737],
        10500: [0., 96.23235541, 160.42803099, 233.55886737, 308.57974206, 355.56444495, 379.04413415, 360.30367399],
        10600: [0., 64.16395093, 112.59864903, 208.95051736, 271.62383941, 310.15832686, 363.97414421, 300.99337804],
        10700: [0., 80.33904057, 122.4292449, 221.99888699, 280.40570234, 332.82317275, 360.96727939, 316.81662093],
        10800: [0., 69.99019905, 111.93263215, 213.27625829, 277.4024096, 326.40536241, 370.08783923, 315.21860948],
        10900: [0., 68.63382741, 116.3546186, 208.87462713, 283.04696926, 326.09234647, 375.63452424, 320.08567823],
        12200: [0., 9.34148917, 99.07126133, 111.73307399, 96.90990572, 212.89047152, 219.51446993, 67.7702778],
        12300: [0., 25.11530581, 108.6181453, 125.07838321, 103.66618766, 217.81901891, 229.67681302, 78.08403441],
        12500: [0., 21.11899415, 97.00897051, 130.03152263, 93.27766257, 208.80160344, 227.84341035, 72.47324398],
        13000: [0., 32.08185638, 91.14300583, 137.36748837, 96.96419238, 231.81677142, 217.76785315, 73.54418181],
        13100: [0., 46.94389583, 101.13778299, 136.09168951, 87.40086664, 244.26926473, 214.21251402, 81.60269703],
        13200: [0., 49.89696527, 119.94065182, 124.88105358, 116.04271674, 231.50802163, 234.45401377, 72.14778894],
    }
    num_antennas = len(tx_antennas)
    phases = np.zeros(num_antennas, dtype=np.complex64)
    if len(tx_antennas) == 16:
        if frequency_khz in cached_values_16_antennas.keys():
            first_half = np.array(cached_values_16_antennas[frequency_khz])
            all_phases = np.concatenate((first_half, np.flip(first_half)))
            phases[tx_antennas] = np.exp(1j * np.deg2rad(all_phases))
            return phases.reshape(1, num_antennas) * 0.999999

    # If you get this far, the number of antennas or frequency is not supported for this function.
    raise ValueError(f"Invalid parameters for easy_widebeam(): tx_antennas: {tx_antennas}, "
                     f"frequency_khz: {frequency_khz}, main_antenna_count: {num_antennas}")


class FullFOV60Deg(ExperimentPrototype):
    def __init__(self, **kwargs):
        """
        kwargs:

        freq: int

        """
        cpid = 3807
        super().__init__(cpid)

        num_ranges = scf.STD_NUM_RANGES

        # default frequency set here
        freq = scf.COMMON_MODE_FREQ_1

        num_antennas = scf.options.main_antenna_count

        slice_0 = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,  # duration of an integration, in ms
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": [[i for i in range(num_antennas)]],
            "tx_beam_order": [0],   # only one pattern
            "tx_antenna_pattern": sixty_deg_widebeam,
            "freq": scf.COMMON_MODE_FREQ_1,  # kHz
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
            #"align_sequences": True,     # align start of sequence to tenths of a second
        }

        slice_1 = copy.deepcopy(slice_0)
        slice_1["freq"] = scf.COMMON_MODE_FREQ_2

        self.add_slice(slice_0)
        self.add_slice(slice_1, interfacing_dict={0: "AVEPERIOD"})