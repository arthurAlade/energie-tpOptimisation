import unittest
from src.scheduling.instance.machine import Machine
from src.scheduling.instance.operation import Operation

class TestMachine(unittest.TestCase):

    def setUp(self):
        self.machine = Machine(
            machine_id=1,
            set_up_time=5,
            set_up_energy=10,
            tear_down_time=3,
            tear_down_energy=6,
            min_consumption=2,
            end_time=100
        )

        self.op1 = Operation(operation_id=1, job_id=1)
        self.op2 = Operation(operation_id=2, job_id=1)

        self.op1.schedule(machine_id=1, at_time=0, duration=10, energy=5)
        self.op2.schedule(machine_id=1, at_time=15, duration=5, energy=2)

    def tearDown(self):
        del self.machine
        del self.op1
        del self.op2

    def testWorkingTime(self):
        self.machine.add_operation(self.op1, start_time=0)
        self.machine.add_operation(self.op2, start_time=10)  # start_time donné, mais add_operation calcule le max

        expected_working_time = self.op1.processing_time + self.op2.processing_time
        self.assertEqual(self.machine.working_time, expected_working_time)

    def testTotalEnergyConsumption(self):
        self.machine.add_operation(self.op1, start_time=0)
        self.machine.add_operation(self.op2, start_time=10)

        expected_energy = (
            self.op1.energy + self.op2.energy + self.machine._set_up_energy + self.machine._tear_down_energy
        )
        self.machine.stop(at_time=30)  # On arrête la machine (ajoute un stop_time)

        self.assertEqual(self.machine.total_energy_consumption, expected_energy)

if __name__ == "__main__":
    unittest.main()
