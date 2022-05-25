from enums import Operators
import globals

memory = globals.memory

expression_operations = {
    Operators.ADD: lambda x, y: int(x) + int(y),
    Operators.MINUS: lambda x, y: int(x) - int(y),
    Operators.DIVIDE: lambda x, y: int(x) / int(y),
    Operators.MULTIPLY: lambda x, y: int(x) * int(y),
    Operators.REL_OP_EQ: lambda x, y: int(x) == int(y),
    Operators.REL_OP_GT: lambda x, y: int(x) > int(y),
    Operators.REL_OP_LT: lambda x, y: int(x) < int(y),
    Operators.REL_OP_NE: lambda x, y: int(x) != int(y),
    Operators.LOG_OP_AND: lambda x, y: x and y,
    Operators.LOG_OP_OR: lambda x, y: x or y,
}


def execute_expression(quadruple):
    operator, address_01, address_02, new_address = quadruple
    value_01 = memory[address_01]
    value_02 = memory[address_02]
    operation = expression_operations[operator]
    result = operation(value_01, value_02)
    memory[new_address] = result
