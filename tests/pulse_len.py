import borealis_experiments.superdarn_common_fields as scf
from utils.experiment_prototype import ExperimentPrototype
from pydantic import ValidationError

from utils.decimation_scheme import (
    create_firwin_filter_by_attenuation,
    DecimationStage,
    DecimationScheme,
)


class PulseLenNotCloseToRxRate(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM + 1,
                "first_range": scf.STD_FIRST_RANGE,
                "num_ranges": scf.STD_NUM_RANGES,
                "intt": scf.INTT_MS,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "rx_beam_order": scf.STD_BEAM_ORDER,
                "tx_beam_order": scf.STD_BEAM_ORDER,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "For an experiment slice with real-time acfs, pulse length must be equal",
        )


class PulseLenDNE(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "first_range": scf.STD_FIRST_RANGE,
                "num_ranges": scf.STD_NUM_RANGES,
                "intt": scf.INTT_MS,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "rx_beam_order": scf.STD_BEAM_ORDER,
                "tx_beam_order": scf.STD_BEAM_ORDER,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "pulse_len\n.*Field required"


class PulseLenNotInt(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": scf.PULSE_LEN_45KM + 0.01,
                "first_range": scf.STD_FIRST_RANGE,
                "num_ranges": scf.STD_NUM_RANGES,
                "intt": scf.INTT_MS,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "rx_beam_order": scf.STD_BEAM_ORDER,
                "tx_beam_order": scf.STD_BEAM_ORDER,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "pulse_len\n.*Input should be a valid integer"


class PulseLenTooLong(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        rates = [5.0e6, 500.0e3, 250.0e3, 50.0e3]
        dm_rates = [10, 2, 5, 5]
        transition_widths = [150.0e3, 40.0e3, 15.0e3, 1.0e3]
        cutoffs = [20.0e3, 10.0e3, 10.0e3, 5.0e3]
        ripple_dbs = [150.0, 80.0, 35.0, 9.0]
        scaling_factors = [10.0, 100.0, 100.0, 100.0]
        all_stages = []
        for stage in range(0, len(rates)):
            filter_taps = list(
                scaling_factors[stage]
                * create_firwin_filter_by_attenuation(
                    rates[stage],
                    transition_widths[stage],
                    cutoffs[stage],
                    ripple_dbs[stage],
                )
            )
            all_stages.append(
                DecimationStage(stage, rates[stage], dm_rates[stage], filter_taps)
            )

        decimation_scheme = DecimationScheme(
            rates[0], rates[-1] / dm_rates[-1], stages=all_stages
        )

        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": 600,
                "pulse_len": 900,
                "first_range": scf.STD_FIRST_RANGE,
                "num_ranges": scf.STD_NUM_RANGES,
                "intt": scf.INTT_MS,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "rx_beam_order": scf.STD_BEAM_ORDER,
                "tx_beam_order": scf.STD_BEAM_ORDER,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
                "decimation_scheme": decimation_scheme,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "Slice 0 pulse length greater than tau_spacing"


class PulseLenTooShort(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        self.add_slice(
            {
                "pulse_sequence": scf.SEQUENCE_7P,
                "tau_spacing": scf.TAU_SPACING_7P,
                "pulse_len": 20,
                "first_range": scf.STD_FIRST_RANGE,
                "num_ranges": scf.STD_NUM_RANGES,
                "intt": scf.INTT_MS,
                "beam_angle": scf.STD_BEAM_ANGLES,
                "rx_beam_order": scf.STD_BEAM_ORDER,
                "tx_beam_order": scf.STD_BEAM_ORDER,
                "freq": scf.COMMON_MODE_FREQ_1,
                "acf": True,
            }
        )

    @classmethod
    def error_message(cls):
        return ValidationError, "Input should be greater than or equal to 100"
