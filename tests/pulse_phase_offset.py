import numpy as np

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
from pydantic import ValidationError


class PhaseEncodingWrongDims(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        def phase_encode(beam_iter, sequence_num, num_pulses):
            return np.random.uniform(-180.0, 180, num_pulses - 1)

        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": 3500,
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
                "pulse_phase_offset": phase_encode,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "pulse_phase_offset\n.*"
            "Value error, Slice 0 Phase encoding return dimension must be equal to number of pulses",
        )


class PhaseEncodingNot1D(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        def phase_encode(beam_iter, sequence_num, num_pulses):
            return np.random.uniform(-180.0, 180, num_pulses).reshape((1, -1))

        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": 3500,
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
                "pulse_phase_offset": phase_encode,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "pulse_phase_offset\n.*"
            "Value error, Slice 0 Phase encoding return must be 1 dimensional",
        )


class PhaseEncodingNotNumpy(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        def phase_encode(beam_iter, sequence_num, num_pulses):
            return np.random.uniform(-180.0, 180, num_pulses).tolist()

        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": 3500,
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
                "pulse_phase_offset": phase_encode,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "pulse_phase_offset\n.*"
            "Value error, Slice 0 Phase encoding return is not numpy array",
        )
