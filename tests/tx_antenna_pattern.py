import numpy as np

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
from pydantic import ValidationError


class TxAntennaPatternWrongDims(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        def antenna_pattern(tx_freq_khz, tx_antennas, antenna_spacing):
            pattern = np.array([1.0 for _ in range(len(tx_antennas) - 1)]).reshape((1, -1))
            return pattern

        self.add_slice({
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": 3500,
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": [scf.STD_16_FORWARD_BEAM_ORDER],
            "tx_beam_order": [0],
            "tx_antenna_pattern": antenna_pattern,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "Slice 0 tx antenna pattern return 2nd dimension \(15\) must be equal to number of main antennas \(16\)"


class TxAntennaPatternMagnitude(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        def antenna_pattern(tx_freq_khz, tx_antennas, antenna_spacing):
            pattern = np.array([1.0 for _ in range(len(tx_antennas))]).reshape((1, -1))
            pattern[0, 0] = 1.01
            return pattern

        self.add_slice({
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": 3500,
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": [scf.STD_16_FORWARD_BEAM_ORDER],
            "tx_beam_order": [0],
            "tx_antenna_pattern": antenna_pattern,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "Slice 0 tx antenna pattern return must not have any values with a magnitude greater than 1"


class TxAntennaPatternNot2D(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        def antenna_pattern(tx_freq_khz, tx_antennas, antenna_spacing):
            pattern = np.array([1.0 for _ in range(len(tx_antennas))])
            return pattern

        self.add_slice({
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": 3500,
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": [scf.STD_16_FORWARD_BEAM_ORDER],
            "tx_beam_order": [0],
            "tx_antenna_pattern": antenna_pattern,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "Slice 0 tx antenna pattern return shape \(16,\) must be 2-dimensional"


class TxAntennaPatternNotNumpy(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        def tx_antenna_pattern(tx_freq_khz, tx_antennas, antenna_spacing):
            pattern = [1.0 for _ in range(len(tx_antennas))]
            return pattern

        self.add_slice({
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": 3500,
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": [scf.STD_16_FORWARD_BEAM_ORDER],
            "tx_beam_order": [0],
            "tx_antenna_pattern": tx_antenna_pattern,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "Slice 0 tx antenna pattern return is not a numpy array"


class TxAntennaPatternNotCallable(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        self.add_slice({
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": 3500,
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": [scf.STD_16_FORWARD_BEAM_ORDER],
            "tx_beam_order": [0],
            "tx_antenna_pattern": "tx_antenna_pattern",
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "tx_antenna_pattern\n.*Input should be callable"
