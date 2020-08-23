from __future__ import print_function


import pytest
import os
from .spec_generator import SpecGenerator
from main import run


def create_spec_file( temp_spec_file, spec_object):
    spec_fobj = open(temp_spec_file, 'w')
    spec_fobj.write(spec_object.create_json())
    spec_fobj.close()


def test_spec_ascii_to_ascii():
    spec_object = SpecGenerator(["Column1", "Column2","Column3"], ["4", "5","10"],
                                "ascii", "True", "ascii")
    temp_spec_file = os.path.join(os.getcwd(), "sample_spec.json")
    try:
        os.remove(temp_spec_file)
    except:
        pass

    create_spec_file(temp_spec_file, spec_object)
    output_csv_file_path = os.path.join(os.getcwd(), "sample_output.csv")
    try:
        os.remove(output_csv_file_path)
    except:
        pass

    input_data = [tuple(["54355sytrjyjut" for _ in range(3)]), tuple(["321wdSF",chr(255), "rdgzxfgsey"])]
    run(input_spec_file=temp_spec_file, input_data=input_data, output_csv_file_path=output_csv_file_path)



