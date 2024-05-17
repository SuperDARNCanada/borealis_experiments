#!/usr/bin/python

"""
Experiment fault: 
    Adding a slice that isn't a dictionary of parameters
"""
from borealis import ExperimentPrototype
from borealis.experiment_prototype.experiment_exception import ExperimentException


class TestExperiment(ExperimentPrototype):

    def __init__(self):
        cpid = 1
        super(TestExperiment, self).__init__(cpid)

        # exp_slice is not a dictionary of slice parameters
        self.add_slice('garbage')

    @classmethod
    def error_message(cls):
        return ExperimentException,\
            "Attempt to add a slice failed - garbage is not a dictionary of slice parameters"
