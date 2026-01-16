import borealis_experiments.superdarn_common_fields as scf
from utils.experiment_prototype import ExperimentPrototype
from utils.exceptions import ExperimentException


class CpidNegative(ExperimentPrototype):
    cpid = -1

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
                "freq": scf.COMMON_MODE_FREQ_1,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "tx_beam_order": scf.STD_BEAM_ORDER,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ExperimentException,
            "The CPID should be a positive number in the experiment. If the embargo"
            " flag is set, then borealis will configure the CPID to be negative to ."
            " indicate the data is to be embargoed for one year.",
        )


class CpidNotInt(ExperimentPrototype):
    cpid = "test"

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
                "freq": scf.COMMON_MODE_FREQ_1,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "tx_beam_order": scf.STD_BEAM_ORDER,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ExperimentException, "CPID must be a unique int"


class CpidNotUnique(ExperimentPrototype):
    cpid = 151  # normalscan

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
                "freq": scf.COMMON_MODE_FREQ_1,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "tx_beam_order": scf.STD_BEAM_ORDER,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ExperimentException,
            "CPID must be unique. 151 is in use by another local experiment",
        )
