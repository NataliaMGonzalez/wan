from re import A
import globals
import raava.common
from enums import FunctionOperators, InstructionPointerJump

memory = globals.memory


def execute_function(quadruple):
    operator: FunctionOperators = quadruple[0]

    if (operator == FunctionOperators.GOSUB):
        current_instruction = raava.common.instruction_pointer
        raava.common.instructions_stack.append(current_instruction)
        new_instruction = quadruple[1]
        raava.common.instruction_pointer = new_instruction - 1

    if (operator == FunctionOperators.RETURN):
        execute_return(quadruple)

    if (operator == FunctionOperators.PUSH_IN_STACK):
        address = quadruple[1]
        saved_value = None
        if(address in memory):
            saved_value = memory[address]
        raava.common.function_stack.append(saved_value)

    if (operator == FunctionOperators.PULL_FROM_STACK):
        address = quadruple[1]
        saved_value = raava.common.function_stack.pop()
        memory[address] = saved_value

    if (operator == FunctionOperators.SAVE_PARAM):
        _, param_address, expression_address = quadruple
        memory[param_address] = memory[expression_address]


def execute_return(quadruple):
    if len(quadruple) > 1:
        _, return_address, expression_address = quadruple
        memory[return_address] = memory[expression_address]
    return_instruction = raava.common.instructions_stack.pop()
    raava.common.instruction_pointer = return_instruction
