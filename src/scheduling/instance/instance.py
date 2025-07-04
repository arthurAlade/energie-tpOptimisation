'''
Information for the instance of the optimization problem.

@author: Vassilissa Lehoux
'''
from typing import List
import os
import csv

from src.scheduling.instance.job import Job
from src.scheduling.instance.operation import Operation
from src.scheduling.instance.machine import Machine


class Instance(object):
    '''
    classdocs
    '''

    def __init__(self, instance_name):
        self._instance_name = instance_name
        self._machines = []
        self._jobs = []
        self._operations = []

    @classmethod
    def from_file(cls, folderpath):
        inst = cls(os.path.basename(folderpath))

        with open(folderpath + os.path.sep + inst._instance_name + '_op.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)
            for row in csv_reader:
                job_id = int(row[0])
                operation_id = int(row[1])

                operation = Operation(operation_id, job_id)
                machine_id = int(row[2])
                processing_time = int(row[3])
                energy = int(row[4])

                start_time = 0
                operation.machine_infos[machine_id] = (processing_time, energy)

                if not any(j.job_id == job_id for j in inst._jobs):
                    inst._jobs.append(Job(job_id))

                for job in inst._jobs:
                    if job.job_id == job_id:
                        job.add_operation(operation)
                        break

                if operation_id not in inst._operations:
                    inst._operations.append(operation)

                for job in inst._jobs:
                    job.operations.sort(key=lambda op: op.operation_id)
                    for i in range(1, len(job.operations)):
                        job.operations[i].previous_operation = job.operations[i - 1]

        # Reading machine info
        with open(folderpath + os.path.sep + inst._instance_name + '_mach.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)
            for row in csv_reader:
                machine_id = int(row[0])
                set_up_time = int(row[1])
                set_up_energy = int(row[2])
                tear_down_time = int(row[3])
                tear_down_energy = int(row[4])
                min_consumption = int(row[5])
                end_time = int(row[6])

                machine = Machine(machine_id, set_up_time, set_up_energy, tear_down_time,
                                  tear_down_energy, min_consumption, end_time)
                inst._machines.append(machine)

        return inst

    @property
    def instance_name(self):
        return self._instance_name

    @instance_name.setter
    def instance_name(self, value):
        self._instance_name = value

    @property
    def name(self):
        return self._instance_name

    @property
    def cmax(self):
        assigned_ops = [op.end_time for op in self._operations if op.assigned]
        return max(assigned_ops) if assigned_ops else 0

    @property
    def sum_ci(self):
        return sum(op.end_time for op in self._operations if op.assigned)

    @property
    def total_energy_consumption(self):
        return sum(op.energy for op in self._operations if op.assigned)

    @property
    def objective(self):
        return self.cmax + self.total_energy_consumption

    @property
    def machines(self) -> List[Machine]:
        return self._machines

    @property
    def jobs(self) -> List[Job]:
        return self._jobs

    @property
    def operations(self) -> List[Operation]:
        return self._operations

    @property
    def nb_jobs(self):
        return len(self._jobs)

    @property
    def nb_machines(self):
        return len(self._machines)

    @property
    def nb_operations(self):
        return len(self._operations)

    def __str__(self):
        return f"{self.name}_M{self.nb_machines}_J{self.nb_jobs}_O{self.nb_operations}"

    def get_machine(self, machine_id) -> Machine:
        for m in self._machines:
            if m.machine_id == machine_id:
                return m
        raise ValueError(f"Machine ID {machine_id} not found")

    def get_job(self, job_id) -> Job:
        for j in self._jobs:
            if j._job_id == job_id:
                return j
        raise ValueError(f"Job ID {job_id} not found")

    def get_operation(self, operation_id) -> Operation:
        for o in self._operations:
            if o.operation_id == operation_id:
                return o
        raise ValueError(f"Operation ID {operation_id} not found")
