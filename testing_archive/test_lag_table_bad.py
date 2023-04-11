#!/usr/bin/python

"""
Experiment fault:
    Adding a pulse that doesn't exist to lag table
"""

import itertools

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
from experiment_prototype.decimation_scheme.decimation_scheme import create_default_scheme
from pydantic import ValidationError


class TestExperiment(ExperimentPrototype):

    def __init__(self):
        cpid = 1
        super(TestExperiment, self).__init__(cpid)

        if scf.IS_FORWARD_RADAR:
            beams_to_use = scf.STD_16_FORWARD_BEAM_ORDER
        else:
            beams_to_use = scf.STD_16_REVERSE_BEAM_ORDER

        if scf.options.site_id in ["cly", "rkn", "inv"]:
            num_ranges = scf.POLARDARN_NUM_RANGES
        if scf.options.site_id in ["sas", "pgr"]:
            num_ranges = scf.STD_NUM_RANGES

        slice_1 = {  # slice_id = 0, there is only one slice.
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": num_ranges,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": 3500,  # duration of an integration, in ms
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": beams_to_use,
            "tx_beam_order": beams_to_use,
            "scanbound": [i * 3.5 for i in range(len(beams_to_use))],   # 1 min scan
            "freq" : scf.COMMON_MODE_FREQ_1,    # kHz
            "acf": True,
            "xcf": True,  # cross-correlation processing
            "acfint": True,  # interferometer acfs
            "decimation_scheme": create_default_scheme(),
        }

        lag_table = list(itertools.combinations(slice_1['pulse_sequence'], 2))
        lag_table.append([slice_1['pulse_sequence'][0], slice_1['pulse_sequence'][0]])  # lag 0
        lag_table.append([99, 0]) ### Should fail on this!!
        # sort by lag number
        lag_table = sorted(lag_table, key=lambda x: x[1] - x[0])
        lag_table.append([slice_1['pulse_sequence'][-1], slice_1['pulse_sequence'][-1]])  # alternate lag 0
        slice_1['lag_table'] = lag_table
        
        self.add_slice(slice_1)

    @classmethod
    def error_message(cls):
        return ValidationError, "Lag \[99, 0\] not valid; One of the pulses does not exist in the sequence. Slice: 0"
