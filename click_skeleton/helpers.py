true_values = ('enabled', 'y', 'yes', 't', 'true', 'True', 'on', '1')
false_values = ('disabled', 'n', 'no', 'f', 'false', 'False', 'off', '0')

def str2bool(val):
    val = str(val).lower()
    if val in true_values:
        return True
    if val in false_values:
        return 0
    raise ValueError(f"invalid truth value {val}")

def str_is_true(v):
    return str(v).lower() in true_values


def str_is_false(v):
    return str(v).lower() in false_values
