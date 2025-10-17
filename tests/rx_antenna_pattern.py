import numpy as np

import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
from pydantic import ValidationError


class RxAntennaPatternWrongDimsIntf(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        def rx_antenna_pattern(beam_angle, freq, antenna_locations):
            """Sets the amplitude and phase weighting for each tx antenna as a list"""
            beam_angle_num = len(beam_angle)
            if antenna_locations.shape[0] == 4:
                beam_angle_num = len(beam_angle) + 1
            pattern = np.array(
                [1.0 for _ in range(antenna_locations.shape[0] * beam_angle_num)]
            )
            pattern = pattern.reshape((beam_angle_num, antenna_locations.shape[0]))
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
                "tx_beam_order": [0],
                "rx_antenna_pattern": rx_antenna_pattern,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "rx_antenna_pattern\n.*Slice 0 interferometer array must be the same shape as \(\[beam angle\], \[antenna_count\]\)",
        )


class RxAntennaPatternMagnitude(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        def rx_antenna_pattern(beam_angle, freq, antenna_locations):
            """Sets the amplitude and phase weighting for each tx antenna"""
            pattern = np.array(
                [1.0 for _ in range(len(beam_angle) * antenna_locations.shape[0])]
            )
            pattern = pattern.reshape((len(beam_angle), antenna_locations.shape[0]))
            pattern[0, 0] = 1.01
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
                "tx_beam_order": [0],
                "rx_antenna_pattern": rx_antenna_pattern,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "rx_antenna_pattern\n.*Slice 0 main array rx antenna pattern return must not have any values with a magnitude greater than 1",
        )


class RxAntennaPatternWrongDimsMain(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        def rx_antenna_pattern(beam_angle, freq, antenna_locations):
            """Sets the amplitude and phase weighting for each tx antenna as a list"""
            pattern = np.array(
                [1.0 for _ in range(antenna_locations.shape[0])]
            ).reshape((1, antenna_locations.shape[0]))
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
                "tx_beam_order": [0],
                "rx_antenna_pattern": rx_antenna_pattern,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "rx_antenna_pattern\n.*Slice 0 main array must be the same shape as \(\[beam angle\], \[antenna_count\]\)",
        )


class RxAntennaPatternNotNumpy(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        def rx_antenna_pattern(beam_angle, freq, antenna_locations):
            """Sets the amplitude and phase weighting for each tx antenna as a list"""
            pattern = [1.0 for _ in range(antenna_locations.shape[0])]
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
                "tx_beam_order": [0],
                "rx_antenna_pattern": rx_antenna_pattern,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "rx_antenna_pattern\n.*Slice 0 main array rx antenna pattern return is not a numpy array",
        )


class RxAntennaPatternNotCallable(ExperimentPrototype):
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
                "rx_beam_order": [scf.STD_16_FORWARD_BEAM_ORDER],
                "tx_beam_order": [0],
                "rx_antenna_pattern": "rx_antenna_pattern",
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "rx_antenna_pattern\n.*Input should be callable"
