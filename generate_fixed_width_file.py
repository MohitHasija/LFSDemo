from __future__ import unicode_literals, print_function
import os
import json
from spec_json import SpecJson
from data_helper import DataReaderAndWriter

INPUT_SPEC_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spec.json")


class FixedWidthFileGenerator(SpecJson, DataReaderAndWriter):

    def __init__(self, input_spec_path):
        # Load the input file in JSON object.
        super().__init__(input_spec_path)
        super(DataReaderAndWriter).__init__()

    def validate_col_names_and_skip(self):
        col_names_list = self.col_names_list
        for i, col_name in enumerate(col_names_list):
            if not self.validate_string_decodes_as_per_given_encoding(self.fixed_width_encoding,
                                                                      string_to_check=col_name):
                print("Column to add: {col_name} is not compatible with given encoding".format(col_name=col_name))
                self.skip(col_name=col_name, col_offset=None)

        return True

    # We assume that if input data element is more than the permissible offset,
    # we just ingest part of the data element.
    def convert_tuple_data_to_restricted_data(self, input_data):

        output_list = []
        #Create col_name to each_entry dictionary.
        data_to_col_names_entry = self.convert_data_to_dictionary(input_data, self.col_names_list)

        for each_col_name, each_offset in self.col_name_to_col_offset.items():
            if each_col_name in self.skipped_elements.keys():
                continue
            each_offset = int(each_offset)
            element = data_to_col_names_entry[each_col_name]
            if each_offset < len(element):
                element = element[:each_offset]
            output_list.append(element)

        return tuple(output_list)

    def write_data(self, fobj, fmt_str, input_data):
        fobj.write(fmt_str % input_data)
        fobj.write('\n')

    def generate_output_for_the_line(self, fobj, fmt_str, data, is_header=False):
        data_to_write = self.validate_incoming_string(self.fixed_width_encoding, data)
        if not is_header:
            self.write_data(fobj=fobj,
                            fmt_str=fmt_str,
                            input_data=self.convert_tuple_data_to_restricted_data(data_to_write)
                            )
        else:
            self.write_data(fobj=fobj,
                            fmt_str=fmt_str,
                            input_data=data_to_write
                            )

    def generate_input_for_csv_parser(self, output_file_path, input_data):
        # At first we check if header has to be added.
        output_fobj = open(output_file_path, mode='w', encoding=self.fixed_width_encoding)
        col_offset_list = [x for x, col_name in zip(self.offset_list, self.col_names_list)
                           if col_name not in self.skipped_elements.keys()
                           ]

        if not col_offset_list:
            print("No column is found valid.")
            output_fobj.close()
            return
        fmt_str = '%' + '%'.join([length + 's' for length in col_offset_list])
        col_names_list = [col_name for col_name in self.col_names_list if col_name not in self.skipped_elements.keys()]
        if self.include_header:
            self.generate_output_for_the_line(output_fobj, fmt_str, tuple(col_names_list), is_header=True)
        for each_tuple in input_data:
            self.generate_output_for_the_line(output_fobj,
                                              fmt_str,
                                              self.convert_tuple_data_to_restricted_data(each_tuple))
        output_fobj.close()



