#!/usr/bin/python

"""
Experiment fault:
    Experiment has no slices
"""

import borealis_experiments.superdarn_common_fields as scf
from borealis import ExperimentPrototype
from borealis import decimation_scheme as dm
from borealis.experiment_prototype.experiment_exception import ExperimentException


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

        ### Don't add any slices

    @classmethod
    def error_message(cls):
        return ExperimentException, "Invalid num_slices less than 1"
