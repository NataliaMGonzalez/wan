def str_to_bool(bool_string: str) -> bool:
    if bool_string == "true":
        return True
    if bool_string == "false":
        return False
    raise Exception("Trying to convert string into boolean.")
