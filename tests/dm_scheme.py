import copy

from utils.decimation_scheme import \
    DecimationScheme, DecimationStage, create_firwin_filter_by_attenuation
import borealis_experiments.superdarn_common_fields as scf
from experiment_prototype.experiment_exception import ExperimentException
from experiment_prototype.experiment_prototype import ExperimentPrototype
from pydantic import ValidationError


class DecimationRateNotInt(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        rates = [5.0e6, 500.0e3, 100.0e3, 50.0e3/3]
        dm_rates = [10.1, 5, 6, 5]  # 10.1 is not an integer, should fail
        transition_widths = [150.0e3, 40.0e3, 15.0e3, 1.0e3]
        cutoffs = [20.0e3, 10.0e3, 10.0e3, 5.0e3]
        ripple_dbs = [150.0, 80.0, 35.0, 9.0]
        scaling_factors = [10.0, 100.0, 100.0, 100.0]
        all_stages = []
        for stage in range(0, len(rates)):
            filter_taps = list(
                scaling_factors[stage] * create_firwin_filter_by_attenuation(
                    rates[stage], transition_widths[stage], cutoffs[stage],
                    ripple_dbs[stage]))
            all_stages.append(DecimationStage(stage, rates[stage],
                              dm_rates[stage], filter_taps))

        # changed from 10e3/3->10e3
        decimation_scheme = (DecimationScheme(rates[0], rates[-1]/dm_rates[-1], stages=all_stages))

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
            "decimation_scheme": decimation_scheme,
        })

    @classmethod
    def error_message(cls):
        return ValueError, "Decimation rate is not an integer"


class DecimationRateRxRateMismatch(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__(rx_bandwidth=1e6)

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
        })

    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "decimation_scheme input data rate 5000000.0 does not match rx_bandwidth 1000000.0"
        )


class FinalStageRxRateMismatch(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        rates = [5.0e6, 500.0e3, 100.0e3, 50.0e3/3]
        dm_rates = [10, 5, 6, 5]
        transition_widths = [150.0e3, 40.0e3, 15.0e3, 1.0e3]
        cutoffs = [20.0e3, 10.0e3, 10.0e3, 5.0e3]
        ripple_dbs = [150.0, 80.0, 35.0, 9.0]
        scaling_factors = [10.0, 100.0, 100.0, 100.0]
        all_stages = []
        for stage in range(0, len(rates)):
            filter_taps = list(
                scaling_factors[stage] * create_firwin_filter_by_attenuation(
                    rates[stage], transition_widths[stage], cutoffs[stage],
                    ripple_dbs[stage]))
            all_stages.append(DecimationStage(stage, rates[stage],
                                              dm_rates[stage], filter_taps))

        # changed from 10e3/3->10e3
        decimation_scheme = (DecimationScheme(rates[0], rates[-2]/dm_rates[-1], stages=all_stages))

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
            "decimation_scheme": decimation_scheme,
        })

    @classmethod
    def error_message(cls):
        return (
            ValueError,
            "Last decimation stage 3 does not have output rate 3333.3333333333335 equal to requested output data "
            "rate 20000.0"
        )


class MismatchedSchemesConcurrent(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        rates = [5.0e6, 500.0e3, 500.0e3/6, 50.0e3/3]
        dm_rates = [10, 6, 5, 5]    # default scheme is [10, 5, 6, 5]
        transition_widths = [150.0e3, 40.0e3, 15.0e3, 1.0e3]
        cutoffs = [20.0e3, 10.0e3, 10.0e3, 5.0e3]
        ripple_dbs = [150.0, 80.0, 35.0, 9.0]
        scaling_factors = [10.0, 100.0, 100.0, 100.0]
        all_stages = []
        for stage in range(0, len(rates)):
            filter_taps = list(
                scaling_factors[stage] * create_firwin_filter_by_attenuation(
                    rates[stage], transition_widths[stage], cutoffs[stage],
                    ripple_dbs[stage]))
            all_stages.append(DecimationStage(stage, rates[stage],
                                              dm_rates[stage], filter_taps))

        # changed from 10e3/3->10e3
        decimation_scheme = (DecimationScheme(rates[0], rates[-1]/dm_rates[-1], stages=all_stages))

        slice_0 = {
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
            "decimation_scheme": decimation_scheme,
        }
        self.add_slice(slice_0)
        slice_1 = copy.deepcopy(slice_0)
        del slice_1['decimation_scheme']
        self.add_slice(slice_1, {0: 'CONCURRENT'})

    @classmethod
    def error_message(cls):
        return (
            ExperimentException,
            "Slices 0 and 1 are CONCURRENT interfaced and do not have the same decimation scheme"
        )


class FirstStageBadInputRate(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        rates = [5.0e6, 500.0e3, 100.0e3, 50.0e3/3]
        dm_rates = [10, 5, 6, 5]
        transition_widths = [150.0e3, 40.0e3, 15.0e3, 1.0e3]
        cutoffs = [20.0e3, 10.0e3, 10.0e3, 5.0e3]
        ripple_dbs = [150.0, 80.0, 35.0, 9.0]
        scaling_factors = [10.0, 100.0, 100.0, 100.0]
        all_stages = []
        for stage in range(0, len(rates)):
            filter_taps = list(
                scaling_factors[stage] * create_firwin_filter_by_attenuation(
                    rates[stage], transition_widths[stage], cutoffs[stage],
                    ripple_dbs[stage]))
            all_stages.append(DecimationStage(stage, rates[stage],
                                              dm_rates[stage], filter_taps))

        # changed from 10e3/3->10e3
        decimation_scheme = (DecimationScheme(5.001e6, rates[-2]/dm_rates[-1], stages=all_stages))

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
            "decimation_scheme": decimation_scheme,
        })

    @classmethod
    def error_message(cls):
        return (
            ValueError,
            "Decimation stage 0 does not have input rate 5000000.0 equal to USRP sampling rate 5001000.0"
        )


class MiddleStageBadInputRate(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

        rates = [5.0e6, 250.0e3, 100.0e3, 50.0e3/3]
        dm_rates = [10, 5, 6, 5]
        transition_widths = [150.0e3, 40.0e3, 15.0e3, 1.0e3]
        cutoffs = [20.0e3, 10.0e3, 10.0e3, 5.0e3]
        ripple_dbs = [150.0, 80.0, 35.0, 9.0]
        scaling_factors = [10.0, 100.0, 100.0, 100.0]
        all_stages = []
        for stage in range(0, len(rates)):
            filter_taps = list(
                scaling_factors[stage] * create_firwin_filter_by_attenuation(
                    rates[stage], transition_widths[stage], cutoffs[stage],
                    ripple_dbs[stage]))
            all_stages.append(DecimationStage(stage, rates[stage],
                                              dm_rates[stage], filter_taps))
        decimation_scheme = (DecimationScheme(rates[0], rates[-1]/dm_rates[-1], stages=all_stages))

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
            "decimation_scheme": decimation_scheme,
        })

    @classmethod
    def error_message(cls):
        return (
            ValueError,
            "Decimation stage 0 output rate 500000.0 does not equal next stage 1 input rate 250000.0"
        )


class FilterTapsNotList(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        rates = [5.0e6, 250.0e3, 100.0e3, 50.0e3/3]
        dm_rates = [10, 5, 6, 5]
        transition_widths = [150.0e3, 40.0e3, 15.0e3, 1.0e3]
        cutoffs = [20.0e3, 10.0e3, 10.0e3, 5.0e3]
        ripple_dbs = [150.0, 80.0, 35.0, 9.0]
        scaling_factors = [10.0, 100.0, 100.0, 100.0]
        all_stages = []
        for stage in range(0, len(rates)):
            filter_taps = list(
                scaling_factors[stage] * create_firwin_filter_by_attenuation(
                    rates[stage], transition_widths[stage], cutoffs[stage],
                    ripple_dbs[stage]))
            all_stages.append(DecimationStage(stage, rates[stage],
                                              dm_rates[stage], set(filter_taps)))

    @classmethod
    def error_message(cls):
        return (
            ValueError,
            "Filter taps {.*} of type <class 'set'> must be a list in decimation stage 0"
        )


class FilterTapsNotNums(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        rates = [5.0e6, 250.0e3, 100.0e3, 50.0e3/3]
        dm_rates = [10, 5, 6, 5]
        transition_widths = [150.0e3, 40.0e3, 15.0e3, 1.0e3]
        cutoffs = [20.0e3, 10.0e3, 10.0e3, 5.0e3]
        ripple_dbs = [150.0, 80.0, 35.0, 9.0]
        scaling_factors = [10.0, 100.0, 100.0, 100.0]
        all_stages = []
        for stage in range(0, len(rates)):
            filter_taps = list(
                scaling_factors[stage] * create_firwin_filter_by_attenuation(
                    rates[stage], transition_widths[stage], cutoffs[stage],
                    ripple_dbs[stage]))
            all_stages.append(DecimationStage(stage, rates[stage],
                                              dm_rates[stage], [str(x) for x in filter_taps]))

    @classmethod
    def error_message(cls):
        return (
            ValueError,
            "Filter tap 1.525146324717017e-08 is not numeric in decimation stage 0"
        )


class TooManyFilterStages(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        rates = [5.0e6, 1.0e6, 500.0e3, 250.0e3, 125.0e3, 62.5e3, 31.25e3 ] # 7 stages, greater than max of 6
        dm_rates = [5, 2, 2, 2, 2, 2, 2]
        transition_widths = [150.0e3, 80.0e3, 40.0e3, 20.0e3, 10.0e3, 5.0e3, 1.0e3]
        cutoffs = [20.0e3, 20.0e3, 10.0e3, 10.0e3, 5.0e3, 5.0e3, 5.0e3]
        ripple_dbs = [150.0, 80.0, 70.0, 35.0, 20.0, 15.0, 10.0]
        scaling_factors = [10.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
        all_stages = []
        for stage in range(0, len(rates)):
            filter_taps = list(
                scaling_factors[stage] * create_firwin_filter_by_attenuation(
                    rates[stage], transition_widths[stage], cutoffs[stage],
                    ripple_dbs[stage]))
            all_stages.append(DecimationStage(stage, rates[stage],
                                              dm_rates[stage], filter_taps))

        decimation_scheme = (DecimationScheme(rates[0], rates[-1]/dm_rates[-1], stages=all_stages))
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
            "decimation_scheme": decimation_scheme,
        })
    @classmethod
    def error_message(cls):
        return (
            ValidationError,
            "Number of decimation stages \(7\) is greater than max available 6"
        )
