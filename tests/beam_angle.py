import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_prototype import ExperimentPrototype
from pydantic import ValidationError


class BeamAngleDNE(ExperimentPrototype):
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
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "beam_angle\n  Field required"


class BeamAngleDuplicates(ExperimentPrototype):
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
            "beam_angle": [-26.25, -26.25, -19.25, -15.75, -12.25, -8.75, -5.25,
                           -1.75, 1.75, 5.25, 8.75, 12.25, 15.75, 19.25, 22.75, 26.25],  # -26.25 duplicated
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "beam_angle\n" \
                                "  Value error, List must have increasing values"


class BeamAngleUnordered(ExperimentPrototype):
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
            "beam_angle": list(reversed(
                [-26.25, -22.75, -19.25, -15.75, -12.25, -8.75, -5.25, -1.75,
                 1.75, 5.25, 8.75, 12.25, 15.75, 19.25, 22.75, 26.25]
            )),
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "beam_angle\n" \
                                "  Value error, List must have increasing values"


class BeamAngleNotList(ExperimentPrototype):
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
            "beam_angle": 3.24,
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "beam_angle\n" \
                                "  Input should be a valid list"


class BeamAngleNotNums(ExperimentPrototype):
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
            "beam_angle": [0, 1.0, '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'],
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        })

    @classmethod
    def error_message(cls):
        return ValidationError, "beam_angle.2\n" \
                                "  Input should be a valid number"
