import copy

import borealis_experiments.superdarn_common_fields as scf
from utils.experiment_prototype import ExperimentPrototype
from utils.exceptions import ExperimentException


class UnknownInterfaceType(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        params = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        }
        self.add_slice(params)
        slice_2 = copy.deepcopy(params)
        slice_2["freq"] = scf.COMMON_MODE_FREQ_2
        self.add_slice(slice_2, interfacing_dict={0: "THISWILLBREAK"})

    @classmethod
    def error_message(cls):
        return (
            ExperimentException,
            "Interface value with slice 0: THISWILLBREAK not valid. Types available are: "
            "\('SCAN', 'AVEPERIOD', 'SEQUENCE', 'CONCURRENT'\)",
        )


class IncompatibleInterfacing(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        params = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        }
        self.add_slice(params)

        slice_2 = copy.deepcopy(params)
        slice_3 = copy.deepcopy(params)
        slice_2["freq"] = scf.COMMON_MODE_FREQ_2
        slice_3["freq"] = scf.COMMON_MODE_FREQ_2 + 1

        # Interfacing between slices is not internally consistent. Here we add slice_2 and slice_3,
        # with CONCURRENT interfacing to slice_1, but then try to interface 2 and 3 together as SCAN.
        self.add_slice(slice_2, interfacing_dict={0: "CONCURRENT"})
        self.add_slice(slice_3, interfacing_dict={0: "CONCURRENT", 1: "SCAN"})

    @classmethod
    def error_message(cls):
        return (
            ExperimentException,
            "The interfacing values of new slice cannot be reconciled. Interfacing with slice 0: CONCURRENT and "
            "with slice 1: SCAN does not make sense with existing interface between slices of None: CONCURRENT",
        )


class InterfaceWithUnknownID(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        params = {
            "pulse_sequence": scf.SEQUENCE_7P,
            "tau_spacing": scf.TAU_SPACING_7P,
            "pulse_len": scf.PULSE_LEN_45KM,
            "num_ranges": scf.STD_NUM_RANGES,
            "first_range": scf.STD_FIRST_RANGE,
            "intt": scf.INTT_7P,
            "beam_angle": scf.STD_16_BEAM_ANGLE,
            "rx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "tx_beam_order": scf.STD_16_FORWARD_BEAM_ORDER,
            "freq": scf.COMMON_MODE_FREQ_1,
            "acf": True,
        }
        self.add_slice(params)
        slice_2 = copy.deepcopy(params)
        slice_2["freq"] = scf.COMMON_MODE_FREQ_2
        # Interfacing dict has interfacing set to an unknown sibling slice ID
        self.add_slice(slice_2, interfacing_dict={99: "SCAN"})

    @classmethod
    def error_message(cls):
        return (
            ExperimentException,
            "Cannot add slice: the interfacing_dict set interfacing to an unknown slice 99 not in slice ids \[0\]",
        )
