'''
Operation of a job.
Its duration and energy consumption depends on the machine on which it is executed.
When operation is scheduled, its schedule information is updated.

@author: Vassilissa Lehoux
'''
from typing import List


class OperationScheduleInfo(object):
    '''
    Informations known when the operation is scheduled
    '''

    def __init__(self, machine_id: int, schedule_time: int, duration: int, energy_consumption: int):
        raise "Not implemented error"


class Operation(object):
    '''
    Operation of the jobs
    '''

    def __init__(self, job_id, operation_id):
        '''
        Constructor
        '''
        self._job_id = job_id
        self._operation_id = operation_id
        self._predecessors = []
        self._successors = []
        self._assigned_to = -1
        self._processing_time = -1
        self._energy = -1
        self._schedule_info = None

    def __str__(self):
        '''
        Returns a string representing the operation.
        '''
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
        if operation not in self._predecessors:
            self._predecessors.append(operation)
            operation.add_successor(self)

    def add_successor(self, operation):
        if operation not in self._successors:
            self._successors.append(operation)
            operation.add_predecessor(self)

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
        return self._assigned_to != -1

    @property
    def assigned_to(self) -> int:
        return self._assigned_to

    @property
    def processing_time(self) -> int:
        return self._processing_time

    @property
    def start_time(self) -> int:
        if self._schedule_info:
            return self._schedule_info.schedule_time
        return -1

    @property
    def end_time(self) -> int:
        if self._schedule_info:
            return self._schedule_info.schedule_time + self._processing_time
        return -1

    @property
    def energy(self) -> int:
        return self._energy if self._assigned_to != -1 else -1

    def is_ready(self, at_time) -> bool:
        for predecessor in self._predecessors:
            if not predecessor.assigned or predecessor.end_time > at_time:
                return False
        return True

    def schedule(self, machine_id: int, at_time: int, check_success=True) -> bool:
        '''
        Schedules an operation. Updates the schedule information of the operation
        @param check_success: if True, check if all the preceeding operations have
          been scheduled and if the schedule time is compatible
        '''
        if self._assigned_to != -1:
            return False
        if check_success and not self.is_ready(at_time):
            return False
        self._assigned_to = machine_id
        self._schedule_info = OperationScheduleInfo(machine_id, at_time, self._processing_time, self._energy)
        return True

    @property
    def min_start_time(self) -> int:
        if not self._predecessors:
            return 0
        return max(predecessor.end_time for predecessor in self._predecessors)

    def schedule_at_min_time(self, machine_id: int, min_time: int) -> bool:
        '''
        Try and schedule the operation af or after min_time.
        Return False if not possible
        '''
        if self._assigned_to != -1:
            return False
        if not self.is_ready(min_time):
            return False
        self._assigned_to = machine_id
        self._schedule_info = OperationScheduleInfo(machine_id, min_time, self._processing_time, self._energy)
        return True
