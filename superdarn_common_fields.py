import sys
import os
import numpy as np

from utils.options import Options
options = Options()

# TODO: We should protect these values from changing, I noticed during testing that I used a
# TODO: call to reverse() on one and it affected the rest of the testing afterwards

STD_RF_RX_RATE = 5.0e6
RX_RATE_45KM = 10.0e3 / 3
RX_RATE_15KM = 10.0e3

SEQUENCE_7P = [0, 9, 12, 20, 22, 26, 27]
TAU_SPACING_7P = 2400  # us
INTT_7P = 3700

SEQUENCE_8P = [0, 14, 22, 24, 27, 31, 42, 43]
TAU_SPACING_8P = 1500  # us
INTT_8P = 3700

STD_8P_LAG_TABLE = [[0, 0],
                    [42, 43],
                    [22, 24],
                    [24, 27],
                    [27, 31],
                    [22, 27],
                    [24, 31],
                    [14, 22],
                    [22, 31],
                    [14, 24],
                    [31, 42],
                    [31, 43],
                    [14, 27],
                    [0, 14],
                    [27, 42],
                    [27, 43],
                    [14, 31],
                    [24, 42],
                    [24, 43],
                    [22, 42],
                    [22, 43],
                    [0, 22],
                    [0, 24],
                    [43, 43]]

PULSE_LEN_45KM = 300  # us
PULSE_LEN_15KM = 100  # us

STD_16_BEAM_ANGLE = [(float(options.beam_sep) * (beam_dir - 15/2)) for beam_dir in range(0, 16)]

STD_NUM_RANGES = 75
POLARDARN_NUM_RANGES = 75
STD_FIRST_RANGE = 180  # km

STD_16_FORWARD_BEAM_ORDER = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
STD_16_REVERSE_BEAM_ORDER = [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

# Scanning directions here for now.
IS_FORWARD_RADAR = IS_REVERSE_RADAR = False
if options.site_id in ["sas", "rkn", "inv"]:
    IS_FORWARD_RADAR = True

if options.site_id in ["cly", "pgr"]:
    IS_REVERSE_RADAR = True

# set common mode operating frequencies with a slight offset.
if options.site_id == "sas":
    COMMON_MODE_FREQ_1 = 10800
    COMMON_MODE_FREQ_2 = 13000
elif options.site_id == "pgr":
    COMMON_MODE_FREQ_1 = 10900
    COMMON_MODE_FREQ_2 = 13100
elif options.site_id == "rkn":
    COMMON_MODE_FREQ_1 = 10600
    COMMON_MODE_FREQ_2 = 12300
elif options.site_id == "inv":
    COMMON_MODE_FREQ_1 = 10500
    COMMON_MODE_FREQ_2 = 12200
elif options.site_id == "cly":
    COMMON_MODE_FREQ_1 = 10700
    COMMON_MODE_FREQ_2 = 12500
else:
    COMMON_MODE_FREQ_1 = 10400
    COMMON_MODE_FREQ_2 = 13200


def easy_scanbound(intt, beams):
    """
    Create integration time boundaries for the scan at the exact
    integration time (intt) boundaries. For new experiments, you
    may wish to ensure that your intt * len(beams) approaches a
    minute mark to reduce delay in waiting for the next scanbound.
    """
    return [i * (intt * 1e-3) for i in range(len(beams))]


# set sounding frequencies
if options.site_id == "sas":
    SOUNDING_FREQS = [9690, 10500, 11000, 11700, 12400, 12900, 13150]
elif options.site_id == "pgr":
    SOUNDING_FREQS = [9600, 10590, 11050, 11750, 13090, 12850, 12400]
elif options.site_id == "rkn":
    SOUNDING_FREQS = [11100, 9600, 10500, 12350, 11800, 13090, 12850]
elif options.site_id == "inv":
    SOUNDING_FREQS = [11150, 9690, 12400, 10590, 11850, 12800, 13100]
elif options.site_id == "cly":
    SOUNDING_FREQS = [11900, 12400, 11100, 10400, 9600, 12800, 13050]
else:
    SOUNDING_FREQS = [10600, 11250, 11950, 13150]


def easy_widebeam(frequency_khz, tx_antennas, antenna_locations):
    """
    Returns phases in degrees for each antenna in the main array that will generate a wide beam pattern
    that illuminates the full FOV. Only 8 or 16 antennas at common frequencies are supported.
    """
    antenna_spacing_m = antenna_locations[1, 0] - antenna_locations[0, 0]  # difference in x-position of first two antennas
    if not np.isclose(antenna_spacing_m, 15.24):
        raise ValueError(f"Antenna spacing must be 15.24m. Given value: {antenna_spacing_m}")

    cached_values_16_antennas = {
        10400: [0.0, 102.96177116, 138.18081147, 222.01613585, 296.53455455, 370.4859424, 391.33134311, 354.02453951,
                 354.02453951, 391.33134311, 370.4859424, 296.53455455, 222.01613585, 138.18081147, 102.96177116, 0.0],
        10500: [0.0, 80.44283403, 109.48744289, 214.83502266, 280.52619912, 335.14851476, 375.59632077, 295.4515181,
                295.4515181, 375.59632077, 335.14851476, 280.52619912, 214.83502266, 109.48744289, 80.44283403, 0.0],
        10600: [0.0, 77.82410539, 105.42021451, 206.22185399, 281.17191033, 333.47601486, 375.83276115, 293.76835248,
                293.76835248, 375.83276115, 333.47601486, 281.17191033, 206.22185399, 105.42021451, 77.82410539, 0.0],
        10700: [0.0, 119.25520118, 154.67891796, 246.09065234, 311.72748683, 382.80492241, 414.82741105, 371.91794781,
                371.91794781, 414.82741105, 382.80492241, 311.72748683, 246.09065234, 154.67891796, 119.25520118, 0.0],
        10800: [0.0, 92.60936645, 127.62619639, 208.5566689, 291.31175873, 354.27697977, 398.79110485, 324.66603882,
                324.66603882, 398.79110485, 354.27697977, 291.31175873, 208.5566689, 127.62619639, 92.60936645, 0.0],
        10900: [0.0, 93.30613356, 125.16534842, 206.51840349, 290.22196672, 355.81710571, 397.82221852, 323.55700502,
                323.55700502, 397.82221852, 355.81710571, 290.22196672, 206.51840349, 125.16534842, 93.30613356, 0.0],
        12200: [0.0, 96.07497475, 208.42258709, 287.2379694, 369.73993686, 440.5011788, 510.15977841, 476.53702585,
                476.53702585, 510.15977841, 440.5011788, 369.73993686, 287.2379694, 208.42258709, 96.07497475, 0.0],
        12300: [0.0, 80.50182428, 196.46546035, 263.58060242, 354.91524796, 433.83518586, 502.04261954, 459.18645715,
                459.18645715, 502.04261954, 433.83518586, 354.91524796, 263.58060242, 196.46546035, 80.50182428, 0.0],
        12500: [0.0, 82.12076029, 196.06309521, 274.07100579, 362.25525702, 440.53954548, 516.49029078, 476.97987124,
                476.97987124, 516.49029078, 440.53954548, 362.25525702, 274.07100579, 196.06309521, 82.12076029, 0.0],
        13000: [0.0, 50.43556708, 120.17720381, 151.36779025, 89.67641224, 225.27830457, 254.59953879, 81.60952527,
                81.60952527, 254.59953879, 225.27830457, 89.67641224, 151.36779025, 120.17720381, 50.43556708, 0.0],
        13100: [0.0, 93.66538642, 205.24967949, 284.06583487, 377.05856963, 443.42958097, 534.86860819, 490.77237812,
                490.77237812, 534.86860819, 443.42958097, 377.05856963, 284.06583487, 205.24967949, 93.66538642, 0.0],
        13200: [0.0, 76.47696612, 154.0441776, 88.27019201, 139.28169901, 230.76759739, 278.5674701, 114.63090199,
                114.63090199, 278.5674701, 230.76759739, 139.28169901, 88.27019201, 154.0441776, 76.47696612, 0.0]
    }
    cached_values_8_antennas = {
        10400: [0., 25.65596691, 78.37293679, 139.64736262, 139.64736262, 78.37293679, 25.65596691, 0.],
        10500: [0., 25.08958919, 77.59100768, 140.85808655, 140.85808655, 77.59100768, 25.08958919, 0.],
        10600: [0., 24.57335302, 76.75481191, 141.98499171, 141.98499171, 76.75481191, 24.57335302, 0.],
        10700: [0., 23.8098711,  75.90392693, 143.01444351, 143.01444351, 75.90392693, 23.8098711,  0.],
        10800: [0., 22.11931133, 73.23562257, 143.47732068, 143.47732068, 73.23562257, 22.11931133, 0.],
        10900: [0., 22.85211015, 72.76130323, 144.37536937, 144.37536937, 72.76130323, 22.85211015, 0.],
        12200: [0., 24.12132192, 67.43277427, 160.59421469, 160.59421469, 67.43277427, 24.12132192, 0.],
        12300: [0., 25.79888664, 68.32548572, 162.24856417, 162.24856417, 68.32548572, 25.79888664, 0.],
        12500: [0., 29.73310292, 70.83940609, 166.04550735, 166.04550735, 70.83940609, 29.73310292, 0.],
        13000: [0., 41.4313578,  82.16477044, 175.25809179, 175.25809179, 82.16477044, 41.4313578,  0.],
        13100: [0., 43.20693263, 84.14234248, 175.38631445, 175.38631445, 84.14234248, 43.20693263, 0.],
        13200: [0., 43.42908842, 84.21675093, 174.68458927, 174.68458927, 84.21675093, 43.42908842, 0.]
    }
    num_antennas = options.main_antenna_count
    phases = np.zeros(num_antennas, dtype=np.complex64)
    if len(tx_antennas) == 16:
        if frequency_khz in cached_values_16_antennas.keys():
            phases[tx_antennas] = np.exp(1j * np.deg2rad(cached_values_16_antennas[frequency_khz]))
            return phases.reshape(1, num_antennas) * 0.999999
    elif len(tx_antennas) == 8:
        if frequency_khz in cached_values_8_antennas.keys():
            phases[tx_antennas] = np.exp(1j * np.deg2rad(cached_values_8_antennas[frequency_khz]))
            return phases.reshape(1, num_antennas) * 0.999999
    # If you get this far, the number of antennas or frequency is not supported for this function.
    raise ValueError(f"Invalid parameters for easy_widebeam(): tx_antennas: {tx_antennas}, "
                     f"frequency_khz: {frequency_khz}, main_antenna_count: {num_antennas}.\n"
                     f"This could be accidental - if you have disconnected a TX channel in your config file, "
                     f"this will reduce the number of transmitting antennas.\nWide transmission beam patterns "
                     f"are very sensitive, so this function only accepts specific operating parameters to produce "
                     f"predictable beam patterns.")
