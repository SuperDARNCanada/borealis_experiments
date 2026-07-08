import borealis_experiments.superdarn_common_fields as scf
from utils.experiment_prototype import ExperimentPrototype
from pydantic import ValidationError
from utils.options import Options

opts = Options()


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
                "intt": scf.INTT_MS,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "rx_beam_order": scf.STD_BEAM_ORDER,
                "tx_beam_order": scf.STD_BEAM_ORDER,
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
                "intt": scf.INTT_MS,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "rx_beam_order": scf.STD_BEAM_ORDER,
                "tx_beam_order": scf.STD_BEAM_ORDER,
                "freq": opts.restricted_ranges[0][1] - 10,  # 10 kHz from top edge of first restricted band
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            f"freq",
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
                "intt": scf.INTT_MS,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "rx_beam_order": scf.STD_BEAM_ORDER,
                "tx_beam_order": scf.STD_BEAM_ORDER,
                "freq": scf.config.max_freq + 1,
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
                "intt": scf.INTT_MS,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "rx_beam_order": scf.STD_BEAM_ORDER,
                "tx_beam_order": scf.STD_BEAM_ORDER,
                "freq": scf.config.min_freq - 1,
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
                "intt": scf.INTT_MS,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "rx_beam_order": scf.STD_BEAM_ORDER,
                "tx_beam_order": scf.STD_BEAM_ORDER,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "Value error, A freq or cfs_range must be specified in a slice. Slice: 0 ",
        )
