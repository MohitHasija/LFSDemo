import json


class SpecGenerator(object):
    def __init__(self, col_names_list,
                 col_offsets_list,
                 fixed_width_encoding,
                 include_header,
                 delimited_encoding):
        self.col_names_list = col_names_list
        self.col_offsets_list = col_offsets_list
        self.fixed_width_encoding = fixed_width_encoding
        self.include_header = include_header
        self.delimted_encoding = delimited_encoding

    def create_json(self):
        json_object = {}
        json_object['ColumnNames'] = self.col_names_list
        json_object['Offsets'] = self.col_offsets_list
        json_object['FixedWidthEncoding'] = self.fixed_width_encoding
        json_object['IncludeHeader'] = self.include_header
        json_object['DelimitedEncoding'] = self.delimted_encoding
        return json.dumps(json_object)
