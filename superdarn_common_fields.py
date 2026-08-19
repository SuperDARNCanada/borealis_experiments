import numpy as np
import json
import os

from utils.options import Options

config = Options()

# TODO: We should protect these values from changing, I noticed during testing that I used a
# TODO: call to reverse() on one and it affected the rest of the testing afterwards

SEQUENCE_7P = [0, 9, 12, 20, 22, 26, 27]
TAU_SPACING_7P = 2400  # us

SEQUENCE_8P = [0, 14, 22, 24, 27, 31, 42, 43]
TAU_SPACING_8P = 1500  # us

STD_8P_LAG_TABLE = [
    [0, 0],
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
    [43, 43],
]

PULSE_LEN_45KM = 300  # us
PULSE_LEN_15KM = 100  # us

STD_FIRST_RANGE = 180  # km
STD_NUM_RANGES = config.num_ranges

STD_BEAM_ANGLES = [
    config.beam_sep * (beam_dir - (config.num_beams - 1) / 2)
    for beam_dir in range(config.num_beams)
]
if config.scan_direction == "clockwise":
    STD_BEAM_ORDER = [i for i in range(config.num_beams)]
elif config.scan_direction == "counterclockwise":
    STD_BEAM_ORDER = list(reversed([i for i in range(config.num_beams)]))
else:
    raise ValueError(
        "Unknown scan direction from config file: expected `clockwise` or `counterclockwise`"
    )

# Calculate integration time per beam, rounded to nearest tenth of a second
INTT_MS = int(600 // config.num_beams) * 100
__integration_time_s__ = INTT_MS / 1000.0

def _load_default_freqs():
    """
    Load the default common-mode and sounding frequencies
    for all configured radar sites. Searches each site 
    configuration file in the Borealis config directory
    and builds a dictionary, mapping each site ID.
    """
    config_dir = os.path.join(os.environ["BOREALISPATH"], "config")
    default_freqs = {}
    for site_id in os.listdir(config_dir):
        config_path = os.path.join(
            config_dir,
            site_id,
            f"{site_id}_config.ini",
        )
        if not os.path.isfile(config_path):
            continue
        with open(config_path, "r") as f:
            site_config = json.load(f)
        if "default_freqs" not in site_config:
            continue
        default_freqs[site_config["site_id"]] = site_config["default_freqs"]
    return default_freqs

__default_freqs__ = _load_default_freqs()

# Get common mode frequencies for the currently operating radar
__site_freqs__ = __default_freqs__[config.site_id]

COMMON_MODE_FREQ_1 = __site_freqs__["common"][0]
COMMON_MODE_FREQ_2 = __site_freqs__["common"][1]
SOUNDING_FREQS = __site_freqs__["sounding"]

def easy_scanbound(intt, beams):
    """
    Create integration time boundaries for the scan at the exact
    integration time (intt) boundaries. For new experiments, you
    may wish to ensure that your intt * len(beams) approaches a
    minute mark to reduce delay in waiting for the next scanbound.
    """
    return [i * (intt * 1e-3) for i in range(len(beams))]


STD_SCANBOUND = easy_scanbound(INTT_MS, STD_BEAM_ANGLES)

_WIDEBEAM_CACHE_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "widebeam_cached_phases.json"
        )

def _load_widebeam_cache(path):
    """
    Load the cached widebeam phase values from JSON
    and freeze them into immutable structures.
    """
    with open(path, "r") as f:
        raw = json.load(f)
    return {
            int(num_antennas): {
                int(freq_khz): tuple(phases) for freq_khz, phases in freq_map.items()
                }
            for num_antennas, freq_map in raw.items()
            }

WIDEBEAM_CACHED_PHASES = _load_widebeam_cache(_WIDEBEAM_CACHE_PATH)

def easy_widebeam(frequency_khz, tx_antennas, antenna_locations):
    """
    Returns phases in degrees for each antenna in the main array that will generate a wide beam pattern
    that illuminates the full FOV. Only 8 or 16 antennas at common frequencies are supported.
    """
    antenna_spacing_m = (
        antenna_locations[1, 0] - antenna_locations[0, 0]
    )  # difference in x-position of first two antennas
    if not np.isclose(antenna_spacing_m, 15.24):
        raise ValueError(
            f"Antenna spacing must be 15.24m. Given value: {antenna_spacing_m}"
        )

    num_antennas = config.main_antenna_count
    phases = np.zeros(num_antennas, dtype=np.complex64)
    
    cached_values = WIDEBEAM_CACHED_PHASES.get(len(tx_antennas))
    if cached_values is not None and frequency_khz in cached_values:
        phases[tx_antennas] = np.exp(
                1j * np.deg2rad(cached_values[frequency_khz])
                )
        return phases.reshape(1, num_antennas) * 0.999999

    # If you get this far, the number of antennas or frequency is not supported for this function.
    raise ValueError(
        f"Invalid parameters for easy_widebeam(): tx_antennas: {tx_antennas}, "
        f"frequency_khz: {frequency_khz}, main_antenna_count: {num_antennas}.\n"
        f"This could be accidental - if you have disconnected a TX channel in your config file, "
        f"this will reduce the number of transmitting antennas.\nWide transmission beam patterns "
        f"are very sensitive, so this function only accepts specific operating parameters to produce "
        f"predictable beam patterns."
    )
