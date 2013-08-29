import filecmp
import os
import sys
import unittest

sys.path.append('../')

from tracetool import trace2csv


def main():
    pass


class Trace2CsvTests(unittest.TestCase):
    def setUp(self):
        self.test_file_1 = 'tracefiles/tracefile_1.tracefile'
        self.test_file_2 = 'tracefiles/tracefile_2.tracefile'
        trace2csv.log2csv(self.test_file_1, include_invalid_packets=False)
        trace2csv.log2csv(self.test_file_2, include_invalid_packets=False)

    def test_file_1_expected_output(self):
        trace2csv_output = 'tracefiles/tracefile_1.csv'
        expected_output = 'tracefiles/tracefile_1_expected_csv.csv'
        self.assertTrue(filecmp.cmp(trace2csv_output, expected_output))

    def test_file_2_expected_output(self):
        trace2csv_output = 'tracefiles/tracefile_2.csv'
        expected_output = 'tracefiles/tracefile_2_expected_csv.csv'
        self.assertTrue(filecmp.cmp(trace2csv_output, expected_output))

    def tearDown(self):
        os.remove('tracefiles/tracefile_1.csv')
        os.remove('tracefiles/tracefile_2.csv')

if __name__ == '__main__':
    main()
