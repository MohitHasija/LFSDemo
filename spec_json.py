import json

class SpecJson(object):
    MAX_OFFSET_PERMITTED = 400

    def __init__(self, spec_json_file):
        # Load the input file in JSON object.
        fobj = open(spec_json_file, 'r')
        spec = json.load(fobj)
        self.col_names_list = spec['ColumnNames']
        self.offset_list = spec['Offsets']
        self.fixed_width_encoding = spec['FixedWidthEncoding']
        self.include_header = spec['IncludeHeader'].lower() == 'true'
        self.delimited_encoding = spec['DelimitedEncoding']
        self.col_name_to_col_offset = dict()
        self.skipped_elements = dict()
        fobj.close()

    def initialise(self):
        for col_name, col_offset in zip(self.col_names_list, self.offset_list):
            self.col_name_to_col_offset[col_name] = col_offset

    def skip_element(self, col_name):
        self.skipped_elements[col_name] = self.col_name_to_col_offset[col_name]
        del self.col_name_to_col_offset[col_name]

    def skip(self, col_name, col_offset):
        if col_name and not col_offset:
            self.skip_element(col_name)
        elif not col_name and col_offset:
            for k, v in self.col_name_to_col_offset.items():
                if v == str(col_offset):
                    self.skip_element(k)
                    return

    def validate_col_names_and_skip(self):
        pass

    def validate_col_offset_and_skip(self):
        col_offset_list = self.offset_list
        for i, col_offset in enumerate(col_offset_list):
            try:
                col_offset = int(col_offset)
                if col_offset > SpecJson.MAX_OFFSET_PERMITTED:
                    print("Incorrect value of offset at index: {index}".format(index=i))
                    # now skip this index value
                    self.skip(col_name=None, col_offset=col_offset)
                continue
            except ValueError as e:
                print(e)
                print("Incorrect format of col_offset provided at index:{d}".format(d=i))
                # now skip this index value
                return False
        return True

    def pre_validate(self):
        self.initialise()
        if self.validate_col_names_and_skip() and self.validate_col_offset_and_skip():
            return True
        return False