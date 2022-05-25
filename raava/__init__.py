import globals
from enums import InputOutputInstructions, Operators
from raava.expressions import execute_expression
from raava.assignments import execute_assignment


memory = globals.memory


def execute(index=0):
    quadruples = globals.quadruples
    quadruple = quadruples[index]
    operator = quadruple[0]
    if isinstance(operator, InputOutputInstructions):
        execute_input_output(quadruple)
    if isinstance(operator, Operators):
        if (operator == Operators.ASSIGN):
            execute_assignment(quadruple)
        else:
            execute_expression(quadruple)

    if index < len(quadruples) - 1:
        execute(index + 1)


def execute_assignment(quadruple):
    _, new_address, original_address, temp_address = quadruple
    memory[new_address] = memory[temp_address] = memory[original_address]


def execute_input_output(quadruple):
    instruction, address = quadruple
    if (instruction == InputOutputInstructions.WRITE):
        print(memory[address])
    if (instruction == InputOutputInstructions.READ):
        memory[address] = input(">> ")
