import globals
import raava.common
from enums import AssignmentOperators, InputOutputInstructions, Operators
from raava.expressions import execute_expression
from raava.assignments import execute_assignment
from raava.input_output import execute_input_output


def execute():
    """ Run all the compiled quadruples of the program. """
    quadruples = globals.quadruples
    while raava.common.instruction_pointer < len(quadruples):
        quadruple = quadruples[raava.common.instruction_pointer]
        execute_quadruple(quadruple)
        raava.common.instruction_pointer += 1


def execute_quadruple(quadruple):
    """ Based on the type of quadruple, run the instructions. """
    operator = quadruple[0]

    if isinstance(operator, InputOutputInstructions):
        execute_input_output(quadruple)

    if isinstance(operator, AssignmentOperators):
        execute_assignment(quadruple)

    if isinstance(operator, Operators):
        execute_expression(quadruple)
