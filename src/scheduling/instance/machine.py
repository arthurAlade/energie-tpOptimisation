'''
Machine on which operation are executed.

@author: Vassilissa Lehoux
'''
from typing import List
from src.scheduling.instance.operation import Operation


class Machine(object):
    '''
    Machine class.
    When operations are scheduled on the machine, contains the relative information. 
    '''

    def __init__(self, machine_id: int, set_up_time: int, set_up_energy: int, tear_down_time: int,
                 tear_down_energy: int, min_consumption: int, end_time: int):
        self._machine_id = machine_id
        self._set_up_time = set_up_time
        self._set_up_energy = set_up_energy
        self._tear_down_time = tear_down_time
        self._tear_down_energy = tear_down_energy
        self._min_consumption = min_consumption
        self._end_time = end_time

        self._operations: List[Operation] = []
        self._start_times: List[int] = []
        self._stop_times: List[int] = []

    def reset(self):
        self._operations = []
        self._start_times = []
        self._stop_times = []

    @property
    def is_feasible(self) -> bool:
        return True

    @property
    def set_up_time(self) -> int:
        return self._set_up_time

    @property
    def tear_down_time(self) -> int:
        return self._tear_down_time

    @property
    def machine_id(self) -> int:
        return self._machine_id

    @property
    def scheduled_operations(self) -> List:
        return self._operations

    @property
    def available_time(self) -> int:
        if not self._operations:
            return 0
        return self._operations[-1].end_time

    def add_operation(self, operation: Operation, start_time: int) -> int:
        # Schedule operation on this machine after start_time
        actual_start_time = max(start_time, self.available_time)
        duration = operation.processing_time
        energy = operation.energy

        # Check if start required
        if not self._operations:
            self._start_times.append(actual_start_time - self._set_up_time)

        # Schedule operation
        operation.schedule(self._machine_id, actual_start_time, duration, energy)
        self._operations.append(operation)

        return actual_start_time

    def stop(self, at_time):
        assert self.available_time <= at_time
        self._stop_times.append(at_time)

    @property
    def working_time(self) -> int:
        return sum([op.processing_time for op in self._operations])

    @property
    def start_times(self) -> List[int]:
        return self._start_times

    @property
    def stop_times(self) -> List[int]:
        return self._stop_times

    @property
    def total_energy_consumption(self) -> int:
        op_energy = sum([op.energy for op in self._operations])
        setup_energy = self._set_up_energy if self._start_times else 0
        teardown_energy = self._tear_down_energy if self._stop_times else 0
        return op_energy + setup_energy + teardown_energy

    def __str__(self):
        return f"M{self.machine_id}"

    def __repr__(self):
        return str(self)