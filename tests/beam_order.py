import copy

import borealis_experiments.superdarn_common_fields as scf
from utils.exceptions import ExperimentException
from utils.experiment_prototype import ExperimentPrototype
from pydantic import ValidationError


class RxBeamOrderDNE(ExperimentPrototype):
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
                "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "rx_beam_order\n  Field required"


class RxBeamOrderValTooLarge(ExperimentPrototype):
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
                "rx_beam_order": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 90],
                "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "rx_beam_order\n.*Value error, Beam number 90 could not index in beam_angle list of length 16. Slice: 0",
        )


class RxBeamOrderNestedValTooLarge(ExperimentPrototype):
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
                "rx_beam_order": [[1, 2, 55], scf.STD_16_FORWARD_BEAM_ORDER],
                "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "rx_beam_order\n.*Value error, Beam number 55 could not index in beam_angle list of length 16. Slice: 0",
        )


class RxBeamOrderNestedValNotInt(ExperimentPrototype):
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
                "rx_beam_order": [["0", "1", "2"], ["hahaha"], ["blah"]],
                "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "Input should be a valid integer"


class RxBeamOrderValsNotInt(ExperimentPrototype):
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
                "rx_beam_order": ["0", "1", "2", "3"],
                "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "Input should be a valid list"


class RxBeamOrderNotList(ExperimentPrototype):
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
                "rx_beam_order": "break_the-beam-order",
                "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "Input should be a valid list"


class RxBeamOrderInterfacing(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        slice_0 = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": 3500,
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        }
        self.add_slice(slice_0)
        slice_1 = copy.deepcopy(slice_0)
        slice_1["rx_beam_order"] = scf.STD_16_FORWARD_BEAM_ORDER[:8]
        slice_1["tx_beam_order"] = scf.STD_16_FORWARD_BEAM_ORDER[:8]
        self.add_slice(slice_1, {0: "SEQUENCE"})

    @classmethod
    def error_message(cls):
        return (
            ExperimentException,
            "Slices 0 and 1 are SEQUENCE or CONCURRENT interfaced but do not have the same number of averaging "
            "periods in their beam order",
        )
