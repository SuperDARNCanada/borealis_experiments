#!/usr/bin/python

"""
Experiment fault:
    Editing a slice without using edit_slice
"""
import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
from experiment_prototype.experiment_utils.decimation_scheme import create_default_scheme


class TestExperiment(ExperimentPrototype):

    def __init__(self):
        cpid = 1
        super().__init__(cpid)

        beams_to_use = scf.STD_16_FORWARD_BEAM_ORDER
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
            "freq": scf.COMMON_MODE_FREQ_1, #kHz
            "decimation_scheme": create_default_scheme(),
        }
        self.add_slice(slice_1)
        setattr(self.slice_dict[0], 'gibberish', 'asdlkfj')
        # self.slice_dict[0].check_slice()

    @classmethod
    def error_message(cls):
        return TypeError, "__init__\(\) got an unexpected keyword argument 'gibberish'"
