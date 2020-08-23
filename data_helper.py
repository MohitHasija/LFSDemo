class DataReaderAndWriter(object):
    def __init__(self):
        pass

    def validate_string_decodes_as_per_given_encoding(self, fmt_encoding, string_to_check):
        try:
            string = string_to_check
            string.encode(fmt_encoding)
            return True
        except Exception as e:
            print(e)
            print("String to add: {string_to_check} is not compatible with given encoding: {encoding}".format(
                string_to_check=string_to_check, encoding=fmt_encoding)
            )
            return False

    def validate_incoming_string(self, encoding, input_tuple):
        input_data = []
        for each_string in input_tuple:
            if not self.validate_string_decodes_as_per_given_encoding(encoding, each_string):
                input_data.append("")
                continue
            input_data.append(each_string)
        input_data = tuple(input_data)
        return input_data

    def convert_data_to_dictionary(self, input_data, col_names_list):
        dict_to_return = {}
        for k,v in zip(col_names_list, input_data):
            dict_to_return[k] = v
        return dict_to_return