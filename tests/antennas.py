import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
from pydantic import ValidationError


class RxIntfAntennaDNE(ExperimentPrototype):
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
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
            "rx_intf_antennas": [0, 1, 2, 18],
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "rx_intf_antennas.3\n.*Input should be less than 16"


class RxIntfAntennaDuplicate(ExperimentPrototype):
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
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
            "rx_intf_antennas": [0, 0, 1, 2],
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "rx_intf_antennas\n.*Value error, List must be unique"


class RxIntfAntennaNegative(ExperimentPrototype):
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
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
            "rx_intf_antennas": [-1, 0, 1, 2],
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "rx_intf_antennas.0\n.*Input should be greater than or equal to 0"


class RxMainAntennaNegative(ExperimentPrototype):
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
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
            "rx_main_antennas": [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16],
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "rx_main_antennas.0\n.*Input should be greater than or equal to 0"


class RxMainAntennaDuplicate(ExperimentPrototype):
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
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
            "rx_main_antennas": [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "rx_main_antennas\n.*Value error, List must be unique"


class RxMainAntennaDNE(ExperimentPrototype):
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
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
            "rx_main_antennas": [0, 1, 2, 3, 4, 5, 6, 7, 8, 23],
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "rx_main_antennas.9\n.*Input should be less than 16"


class TxMainAntennaNegative(ExperimentPrototype):
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
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
            "tx_antennas": [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16],
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "tx_antennas.0\n.*Input should be greater than or equal to 0"


class TxMainAntennaDuplicate(ExperimentPrototype):
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
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
            "tx_antennas": [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "tx_antennas\n.*List should have at most 16 items after validation, not 17"


class TxMainAntennaDNE(ExperimentPrototype):
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
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
            "tx_antennas": [0, 1, 2, 3, 4, 5, 6, 7, 8, 23],
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "tx_antennas.9\n.*Input should be less than 16"


class NoRxMainAntennas(ExperimentPrototype):
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
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
            "rx_main_antennas": [],
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "rx_main_antennas\n.*Value error, Must have at least one main antenna for RX"


class TooManyRxMainAntennas(ExperimentPrototype):
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
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
            "rx_main_antennas": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "rx_main_antennas\n.*List should have at most 16 items after validation, not 17"


class TooManyRxIntfAntennas(ExperimentPrototype):
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
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
            "rx_intf_antennas": [0, 1, 2, 3, 4],
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "rx_intf_antennas\n.*List should have at most 4 items after validation, not 5"


class TooManyTxAntennas(ExperimentPrototype):
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
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
            "tx_antennas": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "tx_antennas\n.*List should have at most 16 items after validation, not 17"
