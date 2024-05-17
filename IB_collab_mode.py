#!/usr/bin/python

"""
    IB_collab_mode
    ~~~~~~~~~~~~~~
    IB collab mode written by Devin Huyghebaert 20200609

    Last scheduled 2020-08-10

    :copyright: 2020 SuperDARN Canada
    :author: Devin Huyghebaert
"""

import datetime

from borealis import ExperimentPrototype
import borealis_experiments.superdarn_common_fields as scf
from borealis import decimation_scheme as dm

def create_15km_scheme():
    """
    Frankenstein script by Devin Huyghebaert for 15 km range gates with
    a special ICEBEAR collab mode

    Built off of the default scheme used for 45 km with minor changes.

    :return DecimationScheme: a decimation scheme for use in experiment.
    """

    rates = [5.0e6, 500.0e3, 100.0e3, 50.0e3]  # last stage 50.0e3/3->50.0e3
    dm_rates = [10, 5, 2, 5]  # third stage 6->2
    transition_widths = [150.0e3, 40.0e3, 15.0e3, 1.0e3]  # did not change
    # bandwidth is double cutoffs.  Did not change
    cutoffs = [20.0e3, 10.0e3, 10.0e3, 5.0e3]
    ripple_dbs = [150.0, 80.0, 35.0, 8.0]  # changed last stage 9->8
    scaling_factors = [10.0, 100.0, 100.0, 100.0]  # did not change
    all_stages = []

    for stage in range(0, len(rates)):
        filter_taps = list(
            scaling_factors[stage] * dm.create_firwin_filter_by_attenuation(
                rates[stage], transition_widths[stage], cutoffs[stage],
                ripple_dbs[stage]))
        all_stages.append(dm.DecimationStage(stage, rates[stage],
                          dm_rates[stage], filter_taps))

    # changed from 10e3/3->10e3
    return (dm.DecimationScheme(rates[0], rates[-1]/dm_rates[-1],
                             stages=all_stages))


class IBCollabMode(ExperimentPrototype):

    def __init__(self, **kwargs):
        """
        kwargs:

        freq: int

        """
        cpid = 3700  # allocated by Marci Detwiller 20200609

        # default frequency set here
        freq = 10800
        
        if kwargs:
            if 'freq' in kwargs.keys():
                freq = int(kwargs['freq'])
                print('Using frequency scheduled for {date}: {freq} kHz'    # TODO: Log
                      .format(date=datetime.datetime.utcnow().strftime('%Y%m%d %H:%M'), freq=freq))
            else:
                print('Frequency not found: using default frequency {freq} kHz'.format(freq=freq))  # TODO: Log
        else:
            print('Frequency not found: using default frequency {freq} kHz'.format(freq=freq))  # TODO: Log

        decimation_scheme = create_15km_scheme()

        bangle = scf.STD_16_BEAM_ANGLE
        beams_arr = [0, 2, 4, 6, 8, 0, 2, 4, 6, 8, 0, 2, 4, 6, 8, 0, 2,
                     4, 6, 8, 0, 2, 4, 6, 8, 0, 2, 4, 6, 8]

        slice_1 = {  # slice_id = 0, the first slice
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_15KM,  # (100 us for 15 km)
            # should only go out to 1500 km w/ 15 km range gates
            "num_ranges": 100,
            "first_range": 90,  # closer than standard first range (180 km)
            "intt": 1900,  # duration of an integration, in ms
            "beam_angle": bangle,
            "rx_beam_order": beams_arr,
            "tx_beam_order": beams_arr,
            "scanbound": [i * 2.0 for i in range(len(beams_arr))],
            "freq": freq,  # kHz
            "txctrfreq": freq + 100,
            "rxctrfreq": freq + 100,
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
            "decimation_scheme": decimation_scheme,
        }

        super().__init__(
            cpid, output_rx_rate=decimation_scheme.output_sample_rate,
            comment_string='ICEBEAR, 5 beam, 2s integration, 15 km')

        self.add_slice(slice_1)
