import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
from pydantic import ValidationError


class NumRangesDNE(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        self.add_slice({
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": 3500,
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq" : scf.COMMON_MODE_FREQ_1,
            "acf": True,
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "num_ranges\n.*Field required"


class NumRangesNotInt(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        self.add_slice({
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "first_range": scf.STD_FIRST_RANGE,
            "num_ranges": '75.5',
            "intt": 3500,
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq" : scf.COMMON_MODE_FREQ_1,
            "acf": True,
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "num_ranges\n.*Input should be a valid integer"
