import borealis_experiments.superdarn_common_fields as scf
from utils.experiment_prototype import ExperimentPrototype
from pydantic import ValidationError


class FreqAboveRxBand(ExperimentPrototype):
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
                "rxctrfreq": 10000.0,
                "freq": 13100.0,  # above rxctrfreq + half the band
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "Slice frequency is outside rx frequency bounds"


class FreqAboveTxBand(ExperimentPrototype):
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
                "txctrfreq": 10000.0,
                "freq": 13100.0,  # above txctrfreq + half the band
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "Slice frequency is outside tx frequency bounds"


class FreqAtRxctrfreq(ExperimentPrototype):
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
                "rxctrfreq": 13125.0,
                "freq": 13100.0,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            f"Slice frequency cannot be within 50kHz of rx center frequency {int(13125.0)}",
        )


class FreqAtTxctrfreq(ExperimentPrototype):
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
                "txctrfreq": 13125.0,
                "freq": 13100.0,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            f"Slice frequency cannot be within 50kHz of tx center frequency {int(13125.0)}",
        )


class FreqBelowRxBand(ExperimentPrototype):
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
                "rxctrfreq": 14000.0,
                "freq": 11300.0,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "Slice frequency is outside rx frequency bounds"


class FreqBelowTxBand(ExperimentPrototype):
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
                "txctrfreq": 14000.0,
                "freq": 11300.0,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "Slice frequency is outside tx frequency bounds"


class FreqNotNum(ExperimentPrototype):
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
                "freq": "twelve thousand",
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "freq.constrained-float\n.*Input should be a valid number",
        )


class FreqRestricted(ExperimentPrototype):
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
                "freq": 13400,  # This should be in a restricted range for the Saskatoon radar
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "freq is within a restricted frequency range \(13155, 13617\)",
        )


class FreqTooHigh(ExperimentPrototype):
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
                "rxctrfreq": 10000.0,
                "freq": scf.options.max_freq + 1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "freq.*\n.*Input should be less than or equal to 20000"


class FreqTooLow(ExperimentPrototype):
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
                "freq": scf.options.min_freq - 1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "freq.*\n.*Input should be less than or equal to 20000"


class FreqDNE(ExperimentPrototype):
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
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "Value error, A freq or cfs_range must be specified in a slice. Slice: 0 ",
        )
