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
        10400: [0., 33.21168501, 63.39856497, 133.51815213, 232.59694556, 287.65482653, 299.43588532, 313.30394893,
                313.30394893, 299.43588532, 287.65482653, 232.59694556, 133.51815213, 63.39856497, 33.21168501, 0.],
        10500: [0., 33.22157987, 63.44769218, 134.09072554, 232.41818196, 288.18043116, 299.96678003, 312.81034918,
                312.81034918, 299.96678003, 288.18043116, 232.41818196, 134.09072554, 63.44769218, 33.22157987, 0.],
        10600: [0., 33.49341546, 63.918406, 135.76673356, 232.41342064, 288.68373728, 299.8089564, 312.19755493,
                312.19755493, 299.8089564, 288.68373728, 232.41342064, 135.76673356, 63.918406, 33.49341546, 0.],
        10700: [0., 33.42706054, 63.94880958, 136.78441366, 232.43324622, 288.91978353, 299.57226291, 311.74840496,
                311.74840496, 299.57226291, 288.91978353, 232.43324622, 136.78441366, 63.94880958, 33.42706054, 0.],
        10800: [0., 33.13909903, 63.56879316, 137.23017826, 232.17488475, 289.01436937, 299.53525025, 311.23785241,
                311.23785241, 299.53525025, 289.01436937, 232.17488475, 137.23017826, 63.56879316, 33.13909903, 0.],
        10900: [0., 33.15305158, 63.55105706, 137.93590292, 232.13550152, 289.46328775, 299.78227805, 310.57614029,
                310.57614029, 299.78227805, 289.46328775, 232.13550152, 137.93590292, 63.55105706, 33.15305158, 0.],
        12200: [0., 70.91038811, 122.60927618, 214.92179098, 276.38784179, 325.25390655, 351.3873793, 316.5693829,
                316.5693829, 351.3873793, 325.25390655, 276.38784179, 214.92179098, 122.60927618, 70.91038811, 0.],
        12300: [0., 71.78224973, 124.29124213, 215.26781585, 277.84490172, 326.57004062, 353.22972278, 318.83181539,
                318.83181539, 353.22972278, 326.57004062, 277.84490172, 215.26781585, 124.29124213, 71.78224973, 0.],
        12500: [0., 75.1870308, 128.12468688, 216.50545923, 281.26273571, 334.23044519, 357.70997722, 326.41420518,
                326.41420518, 357.70997722, 334.23044519, 281.26273571, 216.50545923, 128.12468688, 75.1870308, 0.],
        13000: [0., 65.30441048, 122.04513377, 208.77532736, 282.14858123, 329.88094473, 368.67442895, 324.92709286,
                324.92709286, 368.67442895, 329.88094473, 282.14858123, 208.77532736, 122.04513377, 65.30441048, 0.],
        13100: [0., 75.41723909, 133.59413156, 216.03815626, 287.94258174, 343.50035796, 369.91299149, 337.96682569,
                337.96682569, 369.91299149, 343.50035796, 287.94258174, 216.03815626, 133.59413156, 75.41723909, 0.],
        13200: [0., 67.98474247, 126.21855408, 209.5839628, 285.48610109, 333.17276884, 370.37654775, 329.43903017,
                329.43903017, 370.37654775, 333.17276884, 285.48610109, 209.5839628, 126.21855408, 67.98474247, 0.]
    }
    num_antennas = len(tx_antennas)
    phases = np.zeros(num_antennas, dtype=np.complex64)
    if len(tx_antennas) == 16:
        if frequency_khz in cached_values_16_antennas.keys():
            phases[tx_antennas] = np.exp(1j * np.pi/180. * np.array(cached_values_16_antennas[frequency_khz]))
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