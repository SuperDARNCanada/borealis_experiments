#!/usr/bin/python

"""
    full_fov_interleaved
    ~~~~~~~~~~~~~~
    The mode transmits with a pre-calculated phase progression across the array which illuminates
    a 60-degree FOV, and receives on all antennas. This mode is AVEPERIOD interleaved with narrow-beam scanning
    at the same frequency.

    :copyright: 2024 SuperDARN Canada
    :author: Remington Rohel
"""
import copy

import numpy as np

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype

def sixty_deg_widebeam(frequency_khz, tx_antennas, antenna_locations):
    """
    Returns phases in degrees for each antenna in the main array that will generate a wide beam pattern
    that illuminates a 60-degree FOV. Only 16 antennas at common frequencies is supported.
    """
    antenna_spacing_m = antenna_locations[1, 0] - antenna_locations[0, 0]
    if not np.isclose(antenna_spacing_m, 15.24):
        raise ValueError(f"Antenna spacing must be 15.24m. Given value: {antenna_spacing_m}")

    cached_values_16_antennas = {
        10400: [0., 102.96177116, 138.18081147, 222.01613585, 296.53455455, 370.4859424, 391.33134311, 354.02453951],
        10500: [0., 80.44283403, 109.48744289, 214.83502266, 280.52619912, 335.14851476, 375.59632077, 295.4515181],
        10600: [0., 77.82410539, 105.42021451, 206.22185399, 281.17191033, 333.47601486, 375.83276115, 293.76835248],
        10700: [0., 119.25520118, 154.67891796, 246.09065234, 311.72748683, 382.80492241, 414.82741105, 371.91794781],
        10800: [0., 92.60936645, 127.62619639, 208.5566689, 291.31175873, 354.27697977, 398.79110485, 324.66603882],
        10900: [0., 93.30613356, 125.16534842, 206.51840349, 290.22196672, 355.81710571, 397.82221852, 323.55700502],
        12200: [0., 96.07497475, 208.42258709, 287.2379694, 369.73993686, 440.5011788, 510.15977841, 476.53702585],
        12300: [0., 80.50182428, 196.46546035, 263.58060242, 354.91524796, 433.83518586, 502.04261954, 459.18645715],
        12500: [0., 82.12076029, 196.06309521, 274.07100579, 362.25525702, 440.53954548, 516.49029078, 476.97987124],
        13000: [0., 50.43556708, 120.17720381, 151.36779025, 89.67641224, 225.27830457, 254.59953879, 81.60952527],
        13100: [0., 93.66538642, 205.24967949, 284.06583487, 377.05856963, 443.42958097, 534.86860819, 490.77237812],
        13200: [0., 76.47696612, 154.0441776, 88.27019201, 139.28169901, 230.76759739, 278.5674701, 114.63090199],
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
    raise ValueError(f"Invalid parameters for sixty_deg_widebeam(): tx_antennas: {tx_antennas}, "
                     f"frequency_khz: {frequency_khz}, main_antenna_count: {num_antennas}")


class FullFOVInterleaved(ExperimentPrototype):
    def __init__(self, **kwargs):
        """
        kwargs:

        freq: int

        """
        cpid = 3808
        super().__init__(cpid)

        # default frequency set here
        freq = kwargs.get('freq', scf.COMMON_MODE_FREQ_1)

        slice_0 = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,  # duration of an integration, in ms
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": [[i for i in range(scf.options.main_antenna_count)]],
            "tx_beam_order": [0],   # only one pattern
            "tx_antenna_pattern": sixty_deg_widebeam,
            "freq": freq,  # kHz
            "acf": False,
            # "xcf": True,  # cross-correlation processing
            # "acfint": True,  # interferometer acfs
            #"align_sequences": True,     # align start of sequence to tenths of a second
        }

        slice_1 = copy.deepcopy(slice_0)
        slice_1.pop("tx_antenna_pattern")
        slice_1["rx_beam_order"] = [i for i in range(len(scf.STD_16_BEAM_ANGLE))]
        slice_1["tx_beam_order"] = [i for i in range(len(scf.STD_16_BEAM_ANGLE))]

        self.add_slice(slice_0)
        self.add_slice(slice_1, interfacing_dict={0: "AVEPERIOD"})