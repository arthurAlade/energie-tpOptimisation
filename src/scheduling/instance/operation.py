'''
Operation of a job.
Its duration and energy consumption depends on the machine on which it is executed.
When operation is scheduled, its schedule information is updated.

@author: Vassilissa Lehoux
'''
from typing import List, Optional


class OperationScheduleInfo(object):
    '''
    Informations known when the operation is scheduled
    '''

    def __init__(self, machine_id: int, schedule_time: int, duration: int, energy_consumption: int):
        self.machine_id = machine_id
        self.schedule_time = schedule_time
        self.duration = duration
        self.energy_consumption = energy_consumption

    @property
    def end_time(self):
        return self.schedule_time + self.duration


class Operation(object):
    '''
    Operation of the jobs
    '''

    def __init__(self, operation_id, job_id):
        self._operation_id = operation_id
        self._job_id = job_id
        self._assigned = False
        self._previous_operation = None
        self._schedule_info: Optional[OperationScheduleInfo] = None
        self._predecessors: List[Operation] = []
        self._successors: List[Operation] = []
        self.machine_infos = {}

    def __str__(self):
        base_str = f"O{self.operation_id}_J{self.job_id}"
        if self._schedule_info:
            return base_str + f"_M{self.assigned_to}_ci{self.processing_time}_e{self.energy}"
        else:
            return base_str

    def __repr__(self):
        return str(self)

    def reset(self):
        self._schedule_info = None

    def add_predecessor(self, operation):
        self._predecessors.append(operation)

    def add_successor(self, operation):
        self._successors.append(operation)

    @property
    def operation_id(self) -> int:
        return self._operation_id

    @property
    def job_id(self) -> int:
        return self._job_id

    @property
    def predecessors(self) -> List:
        return self._predecessors

    @property
    def successors(self) -> List:
        return self._successors

    @property
    def assigned(self) -> bool:
        return self._schedule_info is not None

    @property
    def assigned_to(self) -> int:
        return self._schedule_info.machine_id if self.assigned else -1

    @property
    def processing_time(self) -> int:
        return self._schedule_info.duration if self.assigned else -1

    @property
    def start_time(self) -> int:
        return self._schedule_info.schedule_time if self.assigned else -1

    @property
    def end_time(self) -> int:
        return self._schedule_info.end_time if self.assigned else -1

    @property
    def energy(self) -> int:
        return self._schedule_info.energy_consumption if self.assigned else -1

    def is_ready(self, current_time: int) -> bool:
        """
        Vérifie si l'opération est prête à être planifiée :
        - si elle est la première de son job, elle est prête dès t=0
        - sinon, elle est prête seulement si l'opération précédente est terminée
        """
        if self.previous_operation is None:
            return True
        return self.previous_operation.assigned and self.previous_operation.end_time <= current_time

    def schedule(self, machine_id: int, at_time: int, duration: int = -1, energy: int = -1, check_success=True) -> bool:
        if check_success:
            for pred in self._predecessors:
                if not pred.assigned or pred.end_time > at_time:
                    return False
        self._schedule_info = OperationScheduleInfo(machine_id, at_time, duration, energy)
        return True

    @property
    def min_start_time(self) -> int:
        if not self._predecessors:
            return 0
        return max([pred.end_time for pred in self._predecessors if pred.assigned], default=0)

    def schedule_at_min_time(self, machine_id: int, min_time: int, duration: int = -1, energy: int = -1) -> bool:
        min_start = self.min_start_time
        if min_start < min_time:
            min_start = min_time
        return self.schedule(machine_id, min_start, duration, energy)

    @property
    def previous_operation(self):
        return self._previous_operation

    @previous_operation.setter
    def previous_operation(self, operation):
        self._previous_operation = operation

