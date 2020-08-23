from __future__ import unicode_literals, print_function
import os, json
import unittest
from generate_fixed_width_file import FixedWidthFileGenerator, INPUT_SPEC_FILE_PATH
from tests.spec_generator import SpecGenerator

class TestFixedWidthFileGenerator(unittest.TestCase):

    def setUp(self):
        # This is the test data for unit testing
        self.input_spec_file_path = INPUT_SPEC_FILE_PATH
        self.generator_object = FixedWidthFileGenerator(input_spec_path=self.input_spec_file_path)

    def test_generator_init_spec_loaded_correctly(self):
        assert isinstance(self.generator_object.col_names_list, list)
        assert isinstance(self.generator_object.offset_list, list)
        assert isinstance(self.generator_object.fixed_width_encoding, str)
        assert isinstance(self.generator_object.include_header, bool)

    def test_validate_column_names_encoding_compatible_with_given_encoding(self, fixed_width_file_encoding=None):
        if not fixed_width_file_encoding:
            assert self.generator_object.pre_validate()
        else:
            # if we get an encoding format as an input, we can check this value for the sample spec json.
            self.generator_object.fixed_width_encoding = fixed_width_file_encoding
            assert self.generator_object.pre_validate()

    def test_validate_offset_higher_than_permitted_skipped(self):
        self.generator_object.offset_list[4] = str(FixedWidthFileGenerator.MAX_OFFSET_PERMITTED + 1)
        self.generator_object.pre_validate()
        assert len(self.generator_object.col_name_to_col_offset.values()) == 9

    def test_validate_sample_data_with_incompatible_encoding(self):
        self.generator_object.fixed_width_encoding = "ascii"
        sample_col_names_list = [chr(256+i) for i in range(len(self.generator_object.col_names_list))]
        self.generator_object.col_names_list = sample_col_names_list
        self.generator_object.pre_validate()
        assert len(self.generator_object.col_name_to_col_offset.keys()) == 0

    def test_tuple_data_converted_to_restricted_data(self):
        self.generator_object.pre_validate()
        input_data = ("hiii" for _ in range(len(self.generator_object.col_name_to_col_offset.keys())))
        output_data = self.generator_object.convert_tuple_data_to_restricted_data(tuple(input_data))
        assert len(output_data) == 10
        assert output_data[2] == 'hii'
        assert output_data[3] == 'hi'
        assert output_data[0] == 'hiii'

    def test_generate_input_file_for_csv(self):
        self.generator_object.pre_validate()
        input_data = [tuple(["hiii" for _ in range(len(self.generator_object.col_name_to_col_offset.keys()))])]
        output_file_path = os.path.join(os.getcwd(), "sample_output_for_csv_test.txt")
        try:
            self.generator_object.generate_input_for_csv_parser(output_file_path, input_data)
        except Exception as e:
            print(e)
            os.remove(output_file_path)
            assert False
        fobj = open(output_file_path, 'r')
        line = fobj.readline()
        fobj.close()
        #os.remove(output_file_path)
        output_header = '   f1          f2 f3f4           f5     f6        f7           f8                  f9          f10'
        assert line.rstrip() == output_header

class TestFixedWidthFileGeneratorMoreSpec(unittest.TestCase):

    def setUp(self):
        pass

    def test_file_generation_with_all_incorrect_offset(self):
        spec_object = SpecGenerator(["Column1, Column2"], ["4000", "5000"],
                                    "windows-1252", "True", "utf-8")
        temp_spec_file = os.path.join(os.getcwd(), "sample_spec.json")
        self.create_spec_file(temp_spec_file, spec_object)

        generator_object = FixedWidthFileGenerator(input_spec_path=temp_spec_file)
        generator_object.pre_validate()
        output_file_path = os.path.join(os.getcwd(), "sample_output.txt")
        generator_object.generate_input_for_csv_parser(output_file_path=output_file_path,
                                                       input_data=[("hihih", "sample data")])
        sample_output_obj = open(output_file_path, 'r')
        assert len(sample_output_obj.readline()) == 0
        sample_output_obj.close()

    def create_spec_file(self, temp_spec_file, spec_object):

        spec_fobj = open(temp_spec_file, 'w')
        spec_fobj.write(spec_object.create_json())
        spec_fobj.close()


    def test_file_generation_with_one_incorrect_offset(self):
        spec_object = SpecGenerator(["Column1", "Column2"], ["40", "5000"],
                                    "windows-1252", "True", "utf-8")
        temp_spec_file = os.path.join(os.getcwd(), "sample_spec.json")
        self.create_spec_file(temp_spec_file, spec_object)

        generator_object = FixedWidthFileGenerator(input_spec_path=temp_spec_file)
        generator_object.pre_validate()
        output_file_path = os.path.join(os.getcwd(), "sample_output.txt")
        generator_object.generate_input_for_csv_parser(output_file_path=output_file_path,
                                                       input_data=[("hihih", "sample data")])

        # Now check the output
        sample_output_obj = open(output_file_path, 'r')
        line = sample_output_obj.readline()
        sample_output_obj.close()
        assert line.rstrip() == '                                 Column1'

    def test_file_data_generation_with_one_incorrect_offset(self):
        spec_object = SpecGenerator(["Column1", "Column2"], ["40", "5000"],
                                    "windows-1252", "True", "utf-8")
        temp_spec_file = os.path.join(os.getcwd(), "sample_spec.json")
        self.create_spec_file(temp_spec_file, spec_object)

        generator_object = FixedWidthFileGenerator(input_spec_path=temp_spec_file)
        generator_object.pre_validate()
        output_file_path = os.path.join(os.getcwd(), "sample_output.txt")
        generator_object.generate_input_for_csv_parser(output_file_path=output_file_path,
                                                       input_data=[("hihih", "sample data")])

        # Now check the output
        sample_output_obj = open(output_file_path, 'r')
        sample_output_obj.readline()
        line = sample_output_obj.readline()
        sample_output_obj.close()
        assert line.rstrip() == '                                   hihih'




if __name__ == '__main__':
    os.remove(os.path.join(os.getcwd(), "sample_output.txt"))
    os.remove(os.path.join(os.getcwd(), "sample_spec.json"))
    unittest.main()

