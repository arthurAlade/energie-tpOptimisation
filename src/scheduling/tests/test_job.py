'''
Tests for the Job class

@author: Vassilissa Lehoux
'''
import unittest
import os

from src.scheduling.instance.instance import Instance
from src.scheduling.tests.test_utils import TEST_FOLDER_DATA

class TestJob(unittest.TestCase):

    def setUp(self):
        self.inst = Instance.from_file(TEST_FOLDER_DATA + os.path.sep + "jsp1")


    def tearDown(self):
        del self.inst

    def testCompletionTime(self):
        job = self.inst.get_job(0)
        self.assertGreater(len(job.operations), 0, "job sans opérations")

        for i, op in enumerate(job.operations):
            op.schedule(machine_id=1, at_time=i * 10, duration=10, energy=5)

        expected = max(op.end_time for op in job.operations)
        self.assertEqual(job.completion_time, expected)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
