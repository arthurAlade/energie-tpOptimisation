'''
Some useful functions/constants for tests.

@author: Vassilissa Lehoux
'''
import os


TEST_FOLDER = os.path.dirname(os.path.abspath(__file__))
TEST_FOLDER_DATA = TEST_FOLDER + os.path.sep + "data"
TEST_FOLDER_ALL = os.path.abspath(os.path.join(TEST_FOLDER, "..", "..", "..", "data"))
