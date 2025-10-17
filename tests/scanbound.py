import copy

import borealis_experiments.superdarn_common_fields as scf
from utils.exceptions import ExperimentException
from utils.experiment_prototype import ExperimentPrototype
from pydantic import ValidationError


class ScanboundNoIntt(ExperimentPrototype):
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
                "intn": 35,
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "scanbound": [
                    i * 3.5 for i in range(len(scf.STD_16_FORWARD_BEAM_ORDER))
                ],
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "scanbound\n.*Value error, Slice 0 must have intt enabled to use scanbound",
        )


class ScanboundInterfacingScan(ExperimentPrototype):
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
            "scanbound": [i * 3.5 for i in range(len(scf.STD_16_FORWARD_BEAM_ORDER))],
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        }
        self.add_slice(slice_0)
        slice_1 = copy.deepcopy(slice_0)
        del slice_1["scanbound"]
        self.add_slice(slice_1, {0: "SCAN"})

    @classmethod
    def error_message(cls):
        return (
            ExperimentException,
            "If one slice has a scanbound, they all must to avoid up to minute-long downtimes.",
        )


class ScanboundInterfacingSequence(ExperimentPrototype):
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
            "scanbound": [i * 3.5 for i in range(len(scf.STD_16_FORWARD_BEAM_ORDER))],
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        }
        self.add_slice(slice_0)
        slice_1 = copy.deepcopy(slice_0)
        slice_1["scanbound"] = [
            i * 3.6 for i in range(len(scf.STD_16_FORWARD_BEAM_ORDER))
        ]
        self.add_slice(slice_1, {0: "SEQUENCE"})

    @classmethod
    def error_message(cls):
        return (
            ExperimentException,
            "Scan boundary not the same between slices 0 and 1 for AVEPERIOD or CONCURRENT interfaced slices",
        )


class ScanboundNegative(ExperimentPrototype):
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
                "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "scanbound": [
                    i * -3.5 for i in range(len(scf.STD_16_FORWARD_BEAM_ORDER))
                ],
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "scanbound.1\n.*Input should be greater than or equal to 0",
        )


class ScanboundNotIncreasing(ExperimentPrototype):
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
                "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
                "scanbound": list(
                    reversed(
                        [i * 3.5 for i in range(len(scf.STD_16_FORWARD_BEAM_ORDER))]
                    )
                ),
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "scanbound\n.*Value error, List must have increasing values",
        )
