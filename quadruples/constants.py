from lark import Tree
from addresses_manager import assign_constant


def str_to_bool(bool_string: str) -> bool:
    if bool_string == "true":
        return True
    if bool_string == "false":
        return False
    raise Exception("Trying to convert string into boolean.")


def int_constant(self, tree: Tree):
    """Make the appropriate casting and assign the integer into the constants memory.
    Catches the case of a negative value and making the modification.
    """
    is_negative, num = tree.children
    num_value = int(num.value)
    multiplier = -1 if is_negative else 1
    num_value *= multiplier
    address = assign_constant(num_value)
    self.addresses_stack.append(address)


def float_constant(self, tree: Tree):
    """Make the appropriate casting and assign the float into the constants memory.
    Catches the case of a negative value and making the modification.
    """
    is_negative, num = tree.children
    num_value = float(num.value)
    multiplier = -1 if is_negative else 1
    num_value *= multiplier
    address = assign_constant(num_value)
    self.addresses_stack.append(address)


def bool_constant(self, tree: Tree):
    """Make the appropriate casting and assign the bool into the constants memory."""
    bool_str = tree.children[0].value
    bool_value = str_to_bool(bool_str)
    address = assign_constant(bool_value)
    self.addresses_stack.append(address)


def char_constant(self, tree: Tree):
    """Make the appropriate casting and assign the char into the constants memory."""
    char_value = tree.children[0].value[0]
    address = assign_constant(char_value)
    self.addresses_stack.append(address)


def string_constant(self, tree: Tree):
    """Make the appropriate casting and assign the string into the constants memory."""
    string_value = tree.children[0].value
    address = assign_constant(string_value)
    self.addresses_stack.append(address)
