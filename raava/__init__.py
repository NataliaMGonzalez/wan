import globals
from enums import AssignmentOperators, InputOutputInstructions, Operators
from raava.expressions import execute_expression
from raava.assignments import execute_assignment
from raava.input_output import execute_input_output


def execute(index=0):
    """ Based on the type of quadruple, run the instructions. """
    quadruples = globals.quadruples
    quadruple = quadruples[index]
    operator = quadruple[0]

    if isinstance(operator, InputOutputInstructions):
        execute_input_output(quadruple)

    if isinstance(operator, AssignmentOperators):
        execute_assignment(quadruple)

    if isinstance(operator, Operators):
        execute_expression(quadruple)

    if index < len(quadruples) - 1:
        execute(index + 1)
