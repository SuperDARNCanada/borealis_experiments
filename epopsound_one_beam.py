"""
    epopsound_one_beam
    ~~~~~~~~~~~~~~~~~~
    *This is the one-beam version of epopsound (epopsound_one_beam).*

    Experiment for conjunction with EPOP RRI. This mode creates a transmission that is received by
    RRI. 

    Up to 4 frequencies can be used, and given a certain beam range the beams will be cycled through
    at the frequency using 8 pulse sequence, followed by one integration time of a 7 pulse sequence
    at the frequency before moving on to the next frequency. 

    :copyright: 2020 SuperDARN Canada
    :author: Keith Kotyk
"""

import copy
import math

from experiment_prototype.experiment_prototype import ExperimentPrototype
import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.decimation_scheme.decimation_scheme import create_default_scheme


class Epopsound(ExperimentPrototype):

    def __init__(self, **kwargs):
        cpid = 3371

        # default values
        freqs = [scf.COMMON_MODE_FREQ_1]
        beam = 7
        marker_period = 0
        
        if kwargs:
            if 'freq1' in kwargs.keys():
                freqs = [int(kwargs['freq1'])]
                if 'freq2' in kwargs.keys():
                    freqs.append(int(kwargs['freq2']))
                    if 'freq3' in kwargs.keys():
                        freqs.append(int(kwargs['freq3']))
                        if 'freq4' in kwargs.keys():
                            freqs.append(int(kwargs['freq4']))
            if 'beam' in kwargs.keys():
                beam = int(kwargs['beam'])
            if 'marker_period' in kwargs.keys():
                marker_period = int(kwargs['marker_period'])

        print('Freqs (kHz): {}, Beam: {}, Marker Period: {}'.format(freqs, beam, marker_period))    # TODO: Log

        center_freq = int(sum(freqs)/len(freqs))

        if scf.options.site_id in ["cly", "rkn", "inv"]:
            num_ranges = scf.POLARDARN_NUM_RANGES
        if scf.options.site_id in ["sas", "pgr", "lab"]:
            num_ranges = scf.STD_NUM_RANGES

        slices = []
        base_slice = {
            "pulse_sequence": scf.SEQUENCE_8P,
            "tau_spacing": scf.TAU_SPACING_8P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": num_ranges,
            "first_range": scf.STD_FIRST_RANGE,
            "intn": 10,
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "acf": True,
            "xcf": True,
            "acfint": True,
            "decimation_scheme": create_default_scheme(),
        }

        for num, freq in enumerate(freqs):
            # for each freq add 
            new_slice = copy.deepcopy(base_slice)
            new_slice.update({
                "freq": freq
                })

            if marker_period > 0:
                beams_to_use = [beam] * math.floor(marker_period/len(freqs))
                modulus = math.fmod(marker_period, len(freqs))
                if num < modulus:
                    # have to ensure the right num for marker_period
                    beams_to_use.append(beam)
                new_slice.update({
                    "rx_beam_order": beams_to_use,
                    "tx_beam_order": beams_to_use,
                    })
            else:
                new_slice.update({
                    "rx_beam_order": [beam],
                    "tx_beam_order": [beam],
                    })

            slices.append(new_slice)

        super().__init__(cpid=cpid, txctrfreq=center_freq, rxctrfreq=center_freq, comment_string=Epopsound.__doc__)

        self.add_slice(slices[0])
        if len(slices) > 1:
            for a_slice in slices[1:]:
                self.add_slice(a_slice, interfacing_dict={0: 'AVEPERIOD'})

        if marker_period > 0:
            # get the marker slice
            slice_1 = copy.deepcopy(base_slice)
            slice_1.update({
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "rx_beam_order": [beam],
                "tx_beam_order": [beam],
                "freq": freqs[0]
                })
            self.add_slice(slice_1, interfacing_dict={0: 'SCAN'})
