from experiment_prototype.experiment_prototype import ExperimentPrototype
from experiment_prototype.experiment_exception import ExperimentException
import borealis_experiments.superdarn_common_fields as scf


class TxBandwidthNotDivisor(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__(tx_bandwidth=3.14159e6)

    @classmethod
    def error_message(cls):
        return (
            ExperimentException,
            "Experiment's transmit bandwidth 3141590.0 is not possible as it must be an integer divisor of USRP "
            "master clock rate 100000000.0",
        )


class TxBandwidthTooHigh(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__(tx_bandwidth=scf.options.usrp_master_clock_rate / 4)

    @classmethod
    def error_message(cls):
        return (
            ExperimentException,
            "Experiment's transmit bandwidth is too large: 25000000.0 greater than max 5000000.0.",
        )
