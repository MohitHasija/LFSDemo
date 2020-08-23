from __future__ import unicode_literals, print_function
import os, json
import unittest
from generate_fixed_width_file import INPUT_SPEC_FILE_PATH
from create_csv_from_fixed_width_file import CreateCSVFromFixedWidthFile
from tests.spec_generator import SpecGenerator

SAMPLE_INPUT_FILE = os.path.join(os.getcwd(), "sample_output_for_csv_test.txt")

class TestCases(unittest.TestCase):
    def setUp(self):
        self.csv_generator = CreateCSVFromFixedWidthFile(input_fixed_width_file_path=SAMPLE_INPUT_FILE)

    def test_csv_generator_initialised_successfully(self):
        assert isinstance(self.csv_generator.col_names_list, list)
        assert isinstance(self.csv_generator.offset_list, list)
        assert isinstance(self.csv_generator.fixed_width_encoding, str)
        assert isinstance(self.csv_generator.include_header, bool)
        assert isinstance(self.csv_generator.delimited_encoding, str)

    def test_csv_created_from_sample_file(self):
        self.csv_generator.pre_validate()
        output_file_path = os.path.join(os.getcwd(), "sample.csv")
        self.csv_generator.generate_csv(output_file_path)
        output_fobj = open(output_file_path, 'r')
        output_fobj.readline()
        line = output_fobj.readline()
        assert line == "hiii,hiii,hii,hi,hiii,hiii,hiii,hiii,hiii,hiii\n"


if __name__ == '__main__':
    unittest.main()