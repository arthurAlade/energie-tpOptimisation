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



    def testCompletionTime(self):



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
