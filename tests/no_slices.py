from experiment_prototype.experiment_prototype import ExperimentPrototype
from experiment_prototype.experiment_exception import ExperimentException


class NoSlices(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()

    @classmethod
    def error_message(cls):
        return ExperimentException, "Invalid num_slices less than 1"
