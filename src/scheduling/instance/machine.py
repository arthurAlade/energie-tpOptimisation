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
                 tear_down_energy:int, min_consumption: int, end_time: int):
        '''
        Constructor
        Machine is stopped at the beginning of the planning and need to
        be started before executing any operation.
        @param end_time: End of the schedule on this machine: the machine must be
          shut down before that time.
        '''
        self.machine_id = machine_id
        self.set_up_time = set_up_time
        self.set_up_energy = set_up_energy
        self.tear_down_time = tear_down_time
        self.tear_down_energy = tear_down_energy
        self.min_consumption = min_consumption
        self.end_time = end_time
        self._operations = []  # List of scheduled operations
        self._start_times = []  # List of start times of the machine
        self._stop_times = []  # List of stop times of the machine
        self._available_time = 0  # Next time at which the machine is available
        self._total_energy_consumption = 0  # Total energy consumption of the machine

    def reset(self):
        self.machine_id = -1
        self.set_up_time = -1
        self.set_up_energy = -1
        self.tear_down_time = -1
        self.tear_down_energy = -1
        self.min_consumption = -1
        self.end_time = -1
        self._operations = []  # List of scheduled operations
        self._start_times = []  # List of start times of the machine
        self._stop_times = []  # List of stop times of the machine
        self._available_time = -1
        self._total_energy_consumption = -1

    @property
    def set_up_time(self) -> int:
        '''
        Returns the time needed to set up the machine before processing an operation.
        '''
        return self._set_up_time


    @property
    def tear_down_time(self) -> int:
        '''
        Returns the time needed to tear down the machine after processing an operation.
        '''
        return self._tear_down_time

    @property
    def machine_id(self) -> int:
        '''
        Returns the ID of the machine.
        '''
        return self._machine_id

    @property
    def scheduled_operations(self) -> List:
        '''
        Returns the list of the scheduled operations on the machine.
        '''
        return self._operations

    @property
    def available_time(self) -> int:
        """
        Returns the next time at which the machine is available
        after processing its last operation of after its last set up.
        """
        return self._available_time


    def add_operation(self, operation: Operation, start_time: int) -> int:
        '''
        Adds an operation on the machine, at the end of the schedule,
        as soon as possible after time start_time.
        Returns the actual start time.
        '''
        assert(self.available_time <= start_time)
        assert(operation.assigned_to == -1)
        assert(operation.processing_time > 0)
        # Set the operation assigned to this machine
        operation.assigned_to = self.machine_id
        # Set the start time of the operation
        operation.start_time = start_time
        # Set the end time of the operation
        operation.end_time = start_time + operation.processing_time
        # Add the operation to the list of scheduled operations
        self._operations.append(operation)
        # Update the available time of the machine
        self._available_time = operation.end_time
        # Update the total energy consumption of the machine
        self._total_energy_consumption += operation.energy
        # Add the start time of the machine
        self._start_times.append(start_time)
        # Add the stop time of the machine
        self._stop_times.append(operation.end_time)
        # Return the actual start time of the operation
        return operation.start_time


    def stop(self, at_time):
        """
        Stops the machine at time at_time.
        """
        assert(self.available_time >= at_time)
        # Add the stop time of the machine
        self._stop_times.append(at_time)
        # Update the available time of the machine
        self._available_time = at_time + self.tear_down_time
        # Update the total energy consumption of the machine
        self._total_energy_consumption += self.tear_down_energy

    @property
    def working_time(self) -> int:
        '''
        Total time during which the machine is running
        '''
        return sum(op.processing_time for op in self._operations) + \
               len(self._start_times) * self.set_up_time + \
               len(self._stop_times) * self.tear_down_time


    @property
    def start_times(self) -> List[int]:
        """
        Returns the list of the times at which the machine is started
        in increasing order
        """
        return self._start_times

    @property
    def stop_times(self) -> List[int]:
        """
        Returns the list of the times at which the machine is stopped
        in increasing order
        """
        return self._stop_times


    @property
    def total_energy_consumption(self) -> int:
        """
        Total energy consumption of the machine during planning exectution.
        """
        return self._total_energy_consumption + \
               len(self._start_times) * self.set_up_energy + \
               len(self._stop_times) * self.tear_down_energy + \
               len(self._operations) * self.min_consumption

    def __str__(self):
        return f"M{self.machine_id}"

    def __repr__(self):
        return str(self)
