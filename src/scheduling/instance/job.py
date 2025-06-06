'''
Job. It is composed of several operations.

@author: Vassilissa Lehoux
'''
from typing import List, Optional

from src.scheduling.instance.operation import Operation


class Job(object):
    '''
    Job class.
    Contains information on the next operation to schedule for that job
    '''

    def __init__(self, job_id: int):
        self._job_id = job_id
        self._operations: List[Operation] = []
        self._next_index = 0

    @property
    def job_id(self) -> int:
        '''
        Returns the id of the job.
        '''
        return self._job_id

    def reset(self):
        '''
        Resets the planned operations
        '''
        self._next_index = 0
        for op in self._operations:
            op.reset()

    @property
    def operations(self) -> List[Operation]:
        '''
        Returns a list of operations for the job
        '''
        return self._operations

    @property
    def next_operation(self) -> Optional[Operation]:
        '''
        Returns the next operation to be scheduled
        '''
        if self._next_index < len(self._operations):
            return self._operations[self._next_index]
        return None

    def schedule_operation(self):
        '''
        Updates the next_operation to schedule
        '''
        if self._next_index < len(self._operations):
            self._next_index += 1

    @property
    def planned(self):
        '''
        Returns true if all operations are planned
        '''
        return self._next_index >= len(self._operations)

    @property
    def operation_nb(self) -> int:
        '''
        Returns the nb of operations of the job
        '''
        return len(self._operations)

    def add_operation(self, operation: Operation):
        '''
        Adds an operation to the job at the end of the operation list,
        adds the precedence constraints between job operations.
        '''
        if self._operations:
            last_op = self._operations[-1]
            last_op.add_successor(operation)
            operation.add_predecessor(last_op)
        self._operations.append(operation)

    @property
    def completion_time(self) -> int:
        '''
        Returns the job's completion time
        '''
        if not self._operations:
            return 0
        return max(op.end_time for op in self._operations if op.assigned)
