from experiment_prototype.experiment_prototype import ExperimentPrototype
from experiment_prototype.experiment_exception import ExperimentException


class SliceNotDict(ExperimentPrototype):
    cpid = 1

    def __init__(self):
        super().__init__()
        self.add_slice('garbage')

    @classmethod
    def error_message(cls):
        return (
            ExperimentException,
            "Attempt to add a slice failed - garbage is not a dictionary of slice parameters"
        )
