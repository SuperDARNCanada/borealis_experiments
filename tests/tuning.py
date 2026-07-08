import borealis_experiments.superdarn_common_fields as scf
from utils.experiment_prototype import ExperimentPrototype
from pydantic import ValidationError


class AutoTune(ExperimentPrototype):
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
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )


class AutoTuneScan(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        slice_template = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_MS,
            "beam_angle": scf.STD_BEAM_ANGLES,
            "rx_beam_order": scf.STD_BEAM_ORDER,
            "tx_beam_order": scf.STD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        }
        self.add_slice(slice_template)
        slice_template["freq"] = scf.COMMON_MODE_FREQ_2
        self.add_slice(slice_template, interfacing_dict={0: "SCAN"})


class AutoTuneAveperiod(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        slice_template = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_MS,
            "beam_angle": scf.STD_BEAM_ANGLES,
            "rx_beam_order": scf.STD_BEAM_ORDER,
            "tx_beam_order": scf.STD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        }
        self.add_slice(slice_template)
        slice_template["freq"] = scf.COMMON_MODE_FREQ_2
        self.add_slice(slice_template, interfacing_dict={0: "AVEPERIOD"})


class AutoTuneSequence(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        slice_template = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_MS,
            "beam_angle": scf.STD_BEAM_ANGLES,
            "rx_beam_order": scf.STD_BEAM_ORDER,
            "tx_beam_order": scf.STD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        }
        self.add_slice(slice_template)
        slice_template["freq"] = scf.COMMON_MODE_FREQ_2
        self.add_slice(slice_template, interfacing_dict={0: "SEQUENCE"})


class AutoTuneConcurrent(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        slice_template = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_MS,
            "beam_angle": scf.STD_BEAM_ANGLES,
            "rx_beam_order": scf.STD_BEAM_ORDER,
            "tx_beam_order": scf.STD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        }
        self.add_slice(slice_template)
        slice_template["freq"] = scf.COMMON_MODE_FREQ_2
        self.add_slice(slice_template, interfacing_dict={0: "CONCURRENT"})


class TxctrfreqDeprecated(ExperimentPrototype):
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
                "txctrfreq": "ten-thousand",
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "txctrfreq",
        )


class RxctrfreqDeprecated(ExperimentPrototype):
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
                "rxctrfreq": "ten-thousand",
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "rxctrfreq",
        )
