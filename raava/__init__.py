from raava.arrays import execute_array
from raava.utils import execute_goto
from raava.conditionals_cycles import execute_conditionals_cycles
from raava.input_output import execute_input_output
from raava.functions import execute_function
from raava.assignments import execute_assignment
from raava.expressions import execute_expression
from enums import AssignmentOperators, InputOutputInstructions, InstructionPointerJump, Operators, ArrayOperations
from enums import (AssignmentOperators, InputOutputInstructions,
                   InstructionPointerJump, Operators, FunctionOperators)
import globals
import raava.common


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

    if isinstance(operator, InstructionPointerJump):
        execute_conditionals_cycles(quadruple)

    if isinstance(operator, FunctionOperators):
        execute_function(quadruple)

    if (operator == InstructionPointerJump.GOTO):
        execute_goto(quadruple)
    if isinstance(operator, ArrayOperations):
        execute_array(quadruple)
