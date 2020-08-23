import os
import json

from generate_fixed_width_file import FixedWidthFileGenerator
from create_csv_from_fixed_width_file import CreateCSVFromFixedWidthFile

def run(input_spec_file, input_data, output_csv_file_path):
    transient_file_path = os.path.join(os.path.dirname(output_csv_file_path), "fixed_width_file.txt")
    fixed_width_file = FixedWidthFileGenerator(input_spec_path=input_spec_file)
    fixed_width_file.pre_validate()
    fixed_width_file.generate_input_for_csv_parser(output_file_path=transient_file_path,
                                                   input_data=input_data)
    csv_file_generator = CreateCSVFromFixedWidthFile(input_fixed_width_file_path=transient_file_path,
                                                     input_spec_file_path=input_spec_file)
    csv_file_generator.pre_validate()
    csv_file_generator.generate_csv(output_file_path=output_csv_file_path)
    os.remove(transient_file_path)

def main():
    # A sample file run with parameters.
    input_spec_file_path = os.path.join(os.getcwd(), "spec.json")
    input_data = [tuple(["Hiiiiii" for _ in range(10)]), tuple(["Sample" for _ in range(10)])]
    output_csv_file_path = os.path.join(os.getcwd(), "output.csv")
    run(input_spec_file=input_spec_file_path, input_data=input_data, output_csv_file_path=output_csv_file_path)

if __name__=='__main__':
    main()





