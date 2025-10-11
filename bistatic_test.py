#!/usr/bin/python

"""
    bistatic_test
    ~~~~~~~~~~~~~
    The mode transmits with a pre-calculated phase progression across the array which illuminates
    the full FOV, and receives on all antennas. The first pulse in each sequence starts on the 0.1
    second boundaries, to enable bistatic listening on other radars. This mode also chooses a
    frequency from another radar to listen in on, also across the entire FOV simultaneously.

    :copyright: 2022 SuperDARN Canada
    :author: Remington Rohel
"""

import borealis_experiments.superdarn_common_fields as scf
from utils import decimation_scheme as dm
from experiment_prototype.experiment_prototype import ExperimentPrototype


def two_stage_filter():
    """
    Two-stage kaiser window scheme.

    Works well with the following parameters:
    sample_rate = 5e6
    dm_rate = [30, 50]
    transition_width = [150e3, 25e3]
    cutoff_hz = [10e3, 5e3]
    ripple_db = [115, 50]
    """
    sample_rate = 5e6  # 5 MHz
    dm_rate = [30, 50]  # downsampling rates after filters
    transition_width = [150e3, 30e3]  # transition from passband to stopband
    cutoff_hz = [10e3, 5e3]  # bandwidth for output of filter
    ripple_db = [115, 50]  # dB between passband and stopband
    scaling_factors = [1000.0, 10000.0]  # multiplicative factors for each filter stage

    dm_rate_so_far = 1
    stages = []
    for i in range(2):
        rate = sample_rate / dm_rate_so_far
        taps = scaling_factors[i] * dm.create_firwin_filter_by_attenuation(
            rate, transition_width[i], cutoff_hz[i], ripple_db[i]
        )
        stages.append(dm.DecimationStage(i, rate, dm_rate[i], taps.tolist()))
        dm_rate_so_far *= dm_rate[i]

    scheme = dm.DecimationScheme(sample_rate, sample_rate / dm_rate_so_far, stages=stages)

    return scheme


class BistaticTest(ExperimentPrototype):
    """
    This experiment has different behaviour depending on the site that 
    is operating it. SAS, INV, and CLY operate normally (i.e. monostatically),
    while RKN and PGR 'listen in' on CLY, therefore operating as separate
    bistatic systems with CLY. All sites run a widebeam mode that 
    receives (and transmits for some sites) the entire FOV simultaneously.
    """
    def __init__(self, **kwargs):
        """
        kwargs:
            listen_to: str, one of the three-letter site codes. e.g. listen_to='cly'
            beam_order: str, beam order for tx. Only used if listen_to not specified. Format as '1,3,5,6-10',
                which will use beams [1, 3, 5, 6, 7, 8, 9, 10]
        """
        cpid = 3820

        common_freqs = {            # copied from superdarn_common_fields.py - March 2025
            'sas': [10800, 13000],
            'pgr': [10900, 13100],
            'rkn': [10600, 12300],
            'inv': [10500, 12200],
            'cly': [10700, 12500]
        }

        # default frequency set here
        listen_to = kwargs.get('listen_to', scf.options.site_id)   # If 'listen_to' specified, tune in to that radar
        if listen_to not in common_freqs.keys():
            raise ValueError('Not a valid site ID: {}'.format(listen_to))

        freq = common_freqs.get(listen_to)[0]

        slice_0 = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,  # duration of an integration, in ms
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "freq": freq,  # kHz
            "scanbound": [i * 3.7 for i in range(len(scf.STD_16_BEAM_ANGLE))],  # align each aveperiod to 3.7s boundary
            "wait_for_first_scanbound": False,
            "decimation_scheme": two_stage_filter(),
            "align_sequences": True,     # align start of sequence to tenths of a second
        }

        if 'listen_to' in kwargs.keys() and 'beam_order' in kwargs.keys():  # Mutually exclusive arguments
            raise ValueError('ERROR: Cannot specify both "listen_to" and "beam_order".')

        if 'listen_to' not in kwargs.keys():  # Not listening to another radar, so must specify tx characteristics
            # beam_order set here
            if 'beam_order' in kwargs.keys():
                tx_beam_order = []
                beams = kwargs['beam_order'].split(',')
                for beam in beams:
                    # If a range was specified, include all numbers in that range (including endpoints)
                    if '-' in beam:
                        first_beam, last_beam = beam.split('-')
                        tx_beam_order.extend(range(int(first_beam), int(last_beam) + 1))
                    else:
                        tx_beam_order.append(int(beam))
                comment_str = 'Special tx beam order'
            else:
                tx_beam_order = [0]
                slice_0['tx_antenna_pattern'] = scf.easy_widebeam
                comment_str = 'Widebeam transmission'

            slice_0['tx_beam_order'] = tx_beam_order
            rx_beam_order = [[i for i in range(len(scf.STD_16_BEAM_ANGLE))]] * len(tx_beam_order)
            slice_0['rx_beam_order'] = rx_beam_order    # Must have same first dimension as tx_beam_order

        elif listen_to == scf.options.site_id:
            slice_0['rx_beam_order'] = [[i for i in range(len(scf.STD_16_BEAM_ANGLE))]]
            print('Defaulting to rx_only mode, "listen_to" set to this radar')
            comment_str = 'Widebeam listening mode'

        else:
            slice_0['rx_beam_order'] = [[i for i in range(len(scf.STD_16_BEAM_ANGLE))]]
            comment_str = 'Bistatic widebeam mode - listening to {}'.format(listen_to)

        super().__init__(cpid, comment_string=comment_str)

        self.add_slice(slice_0)

