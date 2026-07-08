import borealis_experiments.superdarn_common_fields as scf
from utils.experiment_prototype import ExperimentPrototype
from utils.exceptions import ExperimentException
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


class AutoTuneFreqOrder(ExperimentPrototype):
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
                "rx_beam_order": [0, 1, 0, 1],
                "tx_beam_order": [0, 1, 0, 1],
                "freq": [scf.COMMON_MODE_FREQ_1, scf.COMMON_MODE_FREQ_2],
                "freq_order": [1, 0, 0, 1],
                "acf": True,
            }
        )

class AutoTuneCFS(ExperimentPrototype):
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
                "cfs_range": [scf.COMMON_MODE_FREQ_1, scf.COMMON_MODE_FREQ_1 + 300],
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


class AutoTuneCFSSequence(ExperimentPrototype):
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
            "cfs_range": [scf.COMMON_MODE_FREQ_1, scf.COMMON_MODE_FREQ_1 + 300],
            "acf": True,
        }
        self.add_slice(slice_template)
        slice_template["cfs_range"] = [scf.COMMON_MODE_FREQ_2, scf.COMMON_MODE_FREQ_2 + 300]
        self.add_slice(slice_template, interfacing_dict={0: "SEQUENCE"})


class AutoTuneRegularAndCFS(ExperimentPrototype):
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
        slice_template.pop("freq")
        slice_template["cfs_range"] = [scf.COMMON_MODE_FREQ_2, scf.COMMON_MODE_FREQ_2 + 300]
        self.add_slice(slice_template, interfacing_dict={0: "SEQUENCE"})


class AutoTuneRegularAndFreqOrder(ExperimentPrototype):
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
        slice_template["freq"] = [scf.COMMON_MODE_FREQ_2, scf.COMMON_MODE_FREQ_2 - 300]
        slice_template["freq_order"] = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
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


class AutoTuneFail(ExperimentPrototype):
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
        slice_template["freq"] = scf.COMMON_MODE_FREQ_1 + 8000  # cannot fit in the band, requires retuning
        self.add_slice(slice_template, interfacing_dict={0: "CONCURRENT"})

    @classmethod
    def error_message(cls):
        return (
            ExperimentException,
            "cannot be accommodated with one tuning frequency",
        )


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
