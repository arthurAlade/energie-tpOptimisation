'''
Tests for the Instance class.

@author: Vassilissa Lehoux
'''
import unittest
import os

from src.scheduling.instance.instance import Instance
from src.scheduling.tests.test_utils import TEST_FOLDER_DATA

class TestInstances(unittest.TestCase):

    def setUp(self):
        self.inst = Instance.from_file(TEST_FOLDER_DATA + os.path.sep + "jsp1")

    def tearDown(self):
        del self.inst # reset

    def test_from_file(self):
        self.assertEqual("jsp1", self.inst.name, 'wrong instance name')
        self.assertEqual(4, self.inst.nb_machines, 'wrong nb of machines')
        self.assertEqual(2, self.inst.nb_jobs, 'wrong nb of jobs')
        self.assertEqual(16, self.inst.nb_operations, 'wrong nb of operations')
        self.assertEqual(4, len(self.inst.machines), 'wrong nb of machines')
        self.assertEqual(2, len(self.inst.jobs),  'wrong nb of jobs')
        self.assertEqual('jsp1_M4_J2_O16', str(self.inst), 'wrong string representation of the instance')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
