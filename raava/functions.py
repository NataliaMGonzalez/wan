from re import A
import globals
import raava.common
from enums import FunctionOperators
from raava.memory import (
    assign_into_code_stack, get_address, assign_into_function_stack,
    retreive_from_code_stack, retreive_from_function_stack)

memory = globals.memory


def execute_function(quadruple):
    operator: FunctionOperators = quadruple[0]

    if (operator == FunctionOperators.GOSUB):
        current_instruction = raava.common.instruction_pointer
        assign_into_code_stack(current_instruction)
        new_instruction = quadruple[1]
        raava.common.instruction_pointer = new_instruction - 1

    if (operator == FunctionOperators.RETURN):
        execute_return(quadruple)

    if (operator == FunctionOperators.PUSH_IN_STACK):
        address = quadruple[1]
        saved_value = None
        if(address in memory):
            saved_value = memory[address]
        assign_into_function_stack(saved_value)

    if (operator == FunctionOperators.PULL_FROM_STACK):
        address = quadruple[1]
        saved_value = retreive_from_function_stack()
        memory[address] = saved_value

    if (operator == FunctionOperators.SAVE_PARAM):
        _, param_address, expression_address = quadruple
        memory[param_address] = memory[expression_address]


def execute_return(quadruple):
    if len(quadruple) > 1:
        _, return_address, expression_address = quadruple
        expression_address = get_address(expression_address)
        memory[return_address] = memory[expression_address]
    return_instruction = retreive_from_code_stack()
    raava.common.instruction_pointer = return_instruction
