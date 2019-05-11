import Constants


def remove_string_fillers(string):
    return str(string).replace(Constants.trash_symbol, "")


def fill_string(data, length):
    return data + Constants.trash_symbol * (length - len(data))
