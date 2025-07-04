import unittest
import os

from src.scheduling.instance.instance import Instance
from src.scheduling.solution import Solution
from src.scheduling.tests.test_utils import TEST_FOLDER_DATA, TEST_FOLDER


class TestSolution(unittest.TestCase):

    def setUp(self):
        self.inst = Instance.from_file(TEST_FOLDER_DATA + os.path.sep + "jsp1")

    def tearDown(self):
        del self.inst

    def test_init_sol(self):
        sol = Solution(self.inst)
        self.assertEqual(len(sol.all_operations), len(self.inst._operations),
                        'Nb of operations should be the same between instance and solution')
        self.assertEqual(len(sol.available_operations), len(self.inst._jobs),
                        'One operation per job should be available for scheduling')

    def test_schedule_op(self):
        sol = Solution(self.inst)
        operation = self.inst._operations[0]
        machine = self.inst._machines[1]
        sol.schedule(operation, machine)
        self.assertTrue(operation.assigned, 'operation should be assigned')
        self.assertEqual(operation.assigned_to, 1, 'wrong machine machine')
        self.assertEqual(operation.processing_time, 12, 'wrong operation duration')
        self.assertEqual(operation.energy, 12, 'wrong operation energy cost')
        self.assertEqual(operation.start_time, 20, 'wrong set up time for machine')
        self.assertEqual(operation.end_time, 32, 'wrong operation end time')
        self.assertEqual(machine.available_time, 32, 'wrong available time')
        self.assertEqual(machine.working_time, 120, 'wrong working time for machine')
        operation = self.inst._operations[2]
        sol.schedule(operation, machine)
        self.assertTrue(operation.assigned, 'operation should be assigned')
        self.assertEqual(operation.assigned_to, 1, 'wrong machine machine')
        self.assertEqual(operation.processing_time, 9, 'wrong operation duration')
        self.assertEqual(operation.energy, 10, 'wrong operation energy cost')
        self.assertEqual(operation.start_time, 32, 'wrong start time for operation')
        self.assertEqual(operation.end_time, 41, 'wrong operation end time')
        self.assertEqual(machine.available_time, 41, 'wrong available time')
        self.assertEqual(machine.working_time, 120, 'wrong working time for machine')
        operation = self.inst._operations[1]
        machine = self.inst._machines[0]
        sol.schedule(operation, machine)
        self.assertTrue(operation.assigned, 'operation should be assigned')
        self.assertEqual(operation.assigned_to, 0, 'wrong machine machine')
        self.assertEqual(operation.processing_time, 5, 'wrong operation duration')
        self.assertEqual(operation.energy, 6, 'wrong operation energy cost')
        self.assertEqual(operation.start_time, 32, 'wrong start time for operation')
        self.assertEqual(operation.end_time, 37, 'wrong operation end time')
        self.assertEqual(machine.available_time, 37, 'wrong available time')
        self.assertEqual(machine.working_time, 83, 'wrong working time for machine')
        self.assertEqual(machine.start_times[0], 17)
        self.assertEqual(machine.stop_times[0], 100)
        operation = self.inst._operations[3]
        sol.schedule(operation, machine)
        self.assertTrue(operation.assigned, 'operation should be assigned')
        self.assertEqual(operation.assigned_to, 0, 'wrong machine machine')
        self.assertEqual(operation.processing_time, 10, 'wrong operation duration')
        self.assertEqual(operation.energy, 9, 'wrong operation energy cost')
        self.assertEqual(operation.start_time, 41, 'wrong start time for operation')
        self.assertEqual(operation.end_time, 51, 'wrong operation end time')
        self.assertEqual(machine.available_time, 51, 'wrong available time')
        self.assertEqual(machine.working_time, 83, 'wrong working time for machine')
        self.assertEqual(machine.start_times[0], 17)
        self.assertEqual(machine.stop_times[0], 100)

        self.assertTrue(sol.is_feasible, 'Solution should be feasible')

        # Sauvegarder le diagramme de Gantt (nécessite matplotlib)
        plt = sol.gantt('tab20')
        plt.savefig(TEST_FOLDER + os.path.sep + 'temp.png')

    def test_objective(self):
        '''
        Test your objective function
        '''
        sol = Solution(self.inst)

        obj_val = sol.objective
        self.assertIsInstance(obj_val, (int, float), 'Objective value should be a number')

    def test_schedule_op_2(self):
        job = self.inst.get_job(0)
        operation = job.operations[0]

        operation.machine_infos[0] = (12, 3)

        scheduled = operation.schedule(machine_id=0, at_time=0, duration=12, energy=3, check_success=False)

        self.assertTrue(scheduled, "Schedule should succeed")
        self.assertEqual(operation.processing_time, 12, 'wrong operation duration')


if __name__ == "__main__":
    unittest.main()
