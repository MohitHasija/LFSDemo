import os
import json

from generate_fixed_width_file import INPUT_SPEC_FILE_PATH
from spec_json import SpecJson
from data_helper import DataReaderAndWriter


class CreateCSVFromFixedWidthFile(SpecJson, DataReaderAndWriter):

    def __init__(self, input_fixed_width_file_path, input_spec_file_path=INPUT_SPEC_FILE_PATH):
        super().__init__(input_spec_file_path)
        self.input_file_path = input_fixed_width_file_path
        self.skipped_columns_for_fixed_width = []

    def validate_col_names_and_skip(self):
        col_names_list = self.col_names_list
        for i, col_name in enumerate(col_names_list):
            if not self.validate_string_decodes_as_per_given_encoding(self.delimited_encoding,
                                                                      string_to_check=col_name) \
                    or not self.validate_string_decodes_as_per_given_encoding(self.fixed_width_encoding,
                                                                   string_to_check=col_name):
                print("Column to add: {col_name} is not compatible with given encoding".format(col_name=col_name))
                self.skip(col_name=col_name, col_offset=None)

        return True

    def get_col_names_skipped_for_fixed_width(self):
        col_names_list = self.col_names_list
        for i, col_name in enumerate(col_names_list):
            if not self.validate_string_decodes_as_per_given_encoding(self.fixed_width_encoding, col_name):
                self.skipped_columns_for_fixed_width.append(col_name)

    def generate_output_for_the_line(self,  output_fobj, input_tuple, is_header=False):
        if is_header:
            #let us prepare the columns who will be impacted

            output_fobj.write(','.join(input_tuple) + '\n')
            return
        data_to_write = self.validate_incoming_string(self.delimited_encoding, input_tuple)
        data_to_col_names_entry = self.convert_data_to_dictionary(data_to_write, [x for x in self.col_names_list
                                                                   if x not in self.skipped_elements.keys()])
        refined_data = []
        for each_col_name in self.col_names_list:
            if each_col_name in self.skipped_elements.keys() or each_col_name in self.skipped_columns_for_fixed_width:
                continue
            else:
                refined_data.append(data_to_col_names_entry[each_col_name])
        output_fobj.write(','.join(refined_data) + '\n')

    def generate_csv(self, output_file_path):
        #At first we check if header has to be added.
        output_fobj = open(output_file_path, mode='w', encoding=self.delimited_encoding)
        input_fobj = open(self.input_file_path, mode='r', encoding=self.fixed_width_encoding)
        self.get_col_names_skipped_for_fixed_width()
        col_names_list = [col_name for col_name in self.col_names_list
                          if col_name not in self.skipped_elements.keys() and
                          col_name not in self.skipped_columns_for_fixed_width
                          ]
        if self.include_header:
            input_fobj.readline()
            self.generate_output_for_the_line(output_fobj, tuple(col_names_list), is_header=True)

        for each_line in input_fobj:
            data_list = []
            # Convert each line data to a list
            for each_column_name, each_column_offset in zip(self.col_names_list, self.offset_list):
                if each_column_name in self.skipped_elements.keys():
                    continue
                each_column_offset = int(each_column_offset)
                data_list.append(each_line[:each_column_offset].lstrip())
                each_line = each_line[each_column_offset:]

            self.generate_output_for_the_line(output_fobj, tuple(data_list))
        output_fobj.close()


