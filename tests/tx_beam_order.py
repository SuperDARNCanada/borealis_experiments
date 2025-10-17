import numpy as np

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
from pydantic import ValidationError


class TxBeamOrderMissing(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        def tx_antenna_pattern(tx_freq_khz, tx_antennas, antenna_spacing):
            pattern = np.array([1.0 for _ in range(len(tx_antennas))]).reshape((1, -1))
            return pattern

        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": 3500,
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "rx_beam_order": [scf.STD_16_FORWARD_BEAM_ORDER],
                "tx_antenna_pattern": tx_antenna_pattern,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "1 validation error for ExperimentSlice\n.*Value error, tx_beam_order must be specified if tx_antenna_pattern specified.",
        )


class TxBeamOrderNotInt(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": 3500,
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "tx_beam_order": ["0"],
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "tx_beam_order.*\n.*Input should be a valid integer"


class TxBeamOrderTooLarge(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": 3500,
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "rx_beam_order": [0, 1, 2],
                "tx_beam_order": [0, 1, 22],
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "tx_beam_order\n.*Value error, Slice 0 scan tx beam number 22 DNE",
        )


class TxBeamOrderMismatchPattern(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        def tx_antenna_pattern(tx_freq_khz, tx_antennas, antenna_spacing):
            pattern = np.array([1.0 for _ in range(len(tx_antennas))]).reshape((1, -1))
            return pattern

        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": 3500,
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "rx_beam_order": [
                    scf.STD_16_FORWARD_BEAM_ORDER,
                    scf.STD_16_FORWARD_BEAM_ORDER,
                ],
                "tx_beam_order": [0, 1],
                "tx_antenna_pattern": tx_antenna_pattern,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "tx_beam_order\n.*Value error, Slice 0 scan tx beam number 1 DNE",
        )


class TxBeamOrderMismatchRx(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": 3500,
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "tx_beam_order": [0],
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "tx_beam_order does not have same length as rx_beam_order. Slice: 0",
        )


class TxBeamOrderNotList(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": 3500,
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "tx_beam_order": "break_the-beam-order",
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "tx_beam_order\n.*Input should be a valid list"
