from enums import Operators
import globals
from raava.memory import get_address


memory = globals.memory


EXPRESSION_OPERATIONS = {
    Operators.ADD: lambda x, y: x + y,
    Operators.MINUS: lambda x, y: x - y,
    Operators.DIVIDE: lambda x, y: x / y,
    Operators.MULTIPLY: lambda x, y: x * y,
    Operators.REL_OP_EQ: lambda x, y: x == y,
    Operators.REL_OP_GT: lambda x, y: x > y,
    Operators.REL_OP_GE: lambda x, y: x >= y,
    Operators.REL_OP_LT: lambda x, y: x < y,
    Operators.REL_OP_LE: lambda x, y: x <= y,
    Operators.REL_OP_NE: lambda x, y: x != y,
    Operators.LOG_OP_AND: lambda x, y: x and y,
    Operators.LOG_OP_OR: lambda x, y: x or y,
    Operators.NOT: lambda x: not x,
}


def execute_expression(quadruple: tuple):
    """Executes the instruction that applies to operations."""
    if len(quadruple) == 3:
        execute_unary_expression(quadruple)
        return
    execute_binary_expression(quadruple)


def execute_binary_expression(quadruple: tuple):
    """Executes the expression for binary operators."""
    operator, address_01, address_02, new_address = quadruple
    address_01 = get_address(address_01)
    address_02 = get_address(address_02)
    value_01 = memory[address_01]
    value_02 = memory[address_02]
    operation = EXPRESSION_OPERATIONS[operator]
    result = operation(value_01, value_02)
    memory[new_address] = result


def execute_unary_expression(quadruple: tuple):
    """Executes the expression for unary operators."""
    operator, address, new_address = quadruple
    address = get_address(address)
    value = memory[address]
    operation = EXPRESSION_OPERATIONS[operator]
    result = operation(value)
    memory[new_address] = result
    return
