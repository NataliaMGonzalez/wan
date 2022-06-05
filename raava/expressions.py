from enums import Operators
import globals
from raava.memory import get_address

memory = globals.memory


def cast_to_bool(variable: str):
    if variable == "true":
        return True
    else:
        return False


def and_operation(x: str, y: str):
    """ Logical operation for AND. """
    x = cast_to_bool(x)
    y = cast_to_bool(y)
    return x and y


def or_operation(x: str, y: str):
    """ Logical operation for OR. """
    x = cast_to_bool(x)
    y = cast_to_bool(y)
    return x or y


def not_operation(x: str):
    """ Logical operation for NOT. """
    return not x


EXPRESSION_OPERATIONS = {
    Operators.ADD: lambda x, y: int(x) + int(y),
    Operators.MINUS: lambda x, y: int(x) - int(y),
    Operators.DIVIDE: lambda x, y: int(x) / int(y),
    Operators.MULTIPLY: lambda x, y: int(x) * int(y),
    Operators.REL_OP_EQ: lambda x, y: int(x) == int(y),
    Operators.REL_OP_GT: lambda x, y: int(x) > int(y),
    Operators.REL_OP_GE: lambda x, y: int(x) >= int(y),
    Operators.REL_OP_LT: lambda x, y: int(x) < int(y),
    Operators.REL_OP_LE: lambda x, y: int(x) <= int(y),
    Operators.REL_OP_NE: lambda x, y: int(x) != int(y),
    Operators.LOG_OP_AND: and_operation,
    Operators.LOG_OP_OR: or_operation,
    Operators.NOT: not_operation,
}


def execute_expression(quadruple: tuple):
    """Executes the instruction that applies arithmetic or boolean operations."""
    operator = quadruple[0]
    if operator == Operators.NOT:
        _, address, new_address = quadruple
        address = get_address(address)
        value = memory[address]
        operation = EXPRESSION_OPERATIONS[operator]
        result = operation(value)
        memory[new_address] = result
        return

    operator, address_01, address_02, new_address = quadruple
    address_01 = get_address(address_01)
    address_02 = get_address(address_02)
    value_01 = memory[address_01]
    value_02 = memory[address_02]
    operation = EXPRESSION_OPERATIONS[operator]
    result = operation(value_01, value_02)
    memory[new_address] = result
