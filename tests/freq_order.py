import borealis_experiments.superdarn_common_fields as scf
from utils.experiment_prototype import ExperimentPrototype
from pydantic import ValidationError


class FreqOrderDNE(ExperimentPrototype):
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
                "freq": scf.SOUNDING_FREQS,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "freq_order\n.*multiple freqs specified.*but freq_order not given",
        )


class FreqOrderTooBig(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        beam_order = [0, 1, 2, 3, 4, 5, 6, 7]
        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": 3500,
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "rx_beam_order": beam_order,
                "tx_beam_order": beam_order,
                "freq": scf.SOUNDING_FREQS[:2],
                "freq_order": [0, 1, 0, 1, 0, 1, 0, 2],
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "freq_order\n.*freq_order entries must be in range *[0, 1]",
        )


class FreqOrderTooLong(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        beam_order = [0, 1, 2, 3, 4, 5, 6, 7]
        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": 3500,
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "rx_beam_order": beam_order,
                "tx_beam_order": beam_order,
                "freq": scf.SOUNDING_FREQS[:2],
                "freq_order": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "freq_order\n.*Value error, freq_order must have same length as rx_beam_order \(10 != 8\)",
        )


class FreqOrderTooShort(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        beam_order = [0, 1, 2, 3, 4, 5, 6, 7]
        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM,
                "num_ranges": scf.STD_NUM_RANGES,
                "first_range": scf.STD_FIRST_RANGE,
                "intt": 3500,
                "beam_angle": scf.STD_16_BEAM_ANGLE,
                "rx_beam_order": beam_order,
                "tx_beam_order": beam_order,
                "freq": scf.SOUNDING_FREQS[:2],
                "freq_order": [0, 1, 0, 1],
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "freq_order\n.*Value error, freq_order must have same length as rx_beam_order \(4 != 8\)",
        )


class FreqOrderWithCFS(ExperimentPrototype):
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
                "cfs_range": [12000, 12300],
                "freq_order": [0, 1],
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "freq_order\n.*Value error, Cannot specify freq_order if using CFS",
        )
