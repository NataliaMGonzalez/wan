import globals
import raava.common
from enums import FunctionOperators, InstructionPointerJump

memory = globals.memory


def execute_function(quadruple):
    operator: FunctionOperators = quadruple[0]

    if (operator == FunctionOperators.GOSUB):
        current_instruction = raava.common.instruction_pointer
        raava.common.return_to_instruction = current_instruction
        function_position = quadruple[1]
        raava.common.instruction_pointer = function_position - 1

    if (operator == FunctionOperators.RETURN):
        _, return_address, expression_address = quadruple
        memory[return_address] = memory[expression_address]
        return_instruction = raava.common.return_to_instruction
        raava.common.instruction_pointer = return_instruction - 1

    if (operator == FunctionOperators.PUSH_IN_STACK):
        address = quadruple[1]
        raava.common.function_stack.append(address)

    if (operator == FunctionOperators.PULL_FROM_STACK):
        address = quadruple[1]
        memory[address] = raava.common.function_stack.pop()

    if (operator == FunctionOperators.SAVE_PARAM):
        _, param_address, expression_address = quadruple
        memory[param_address] = memory[expression_address]
