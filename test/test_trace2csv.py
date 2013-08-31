import filecmp
import os
import sys
import unittest

sys.path.append('../')

from tracetool import trace2csv


INPUT_FILE_1 = 'tracefiles/tracefile_1.tracefile'
INPUT_FILE_2 = 'tracefiles/tracefile_2.tracefile'
OUTPUT_FILE_1 = 'tracefiles/tracefile_1.csv'
OUTPUT_FILE_2 = 'tracefiles/tracefile_2.csv'
EXPECTED_OUTPUT_1 = 'tracefiles/tracefile_1_expected_csv.csv'
EXPECTED_OUTPUT_2 = 'tracefiles/tracefile_2_expected_csv.csv'
READER_FILE = 'tracefiles/tracefile_reader.py'


class Trace2CsvTests(unittest.TestCase):
    def test_file_1_expected_output(self):
        trace2csv.trace2csv(INPUT_FILE_1, READER_FILE)
        self.assertTrue(filecmp.cmp(OUTPUT_FILE_1, EXPECTED_OUTPUT_1))

    def test_file_2_expected_output(self):
        trace2csv.trace2csv(INPUT_FILE_2, READER_FILE)
        self.assertTrue(filecmp.cmp(OUTPUT_FILE_2, EXPECTED_OUTPUT_2))

    def tearDown(self):
        if os.path.isfile(OUTPUT_FILE_1):
            os.remove(OUTPUT_FILE_1)
        if os.path.isfile(OUTPUT_FILE_2):
            os.remove(OUTPUT_FILE_2)
