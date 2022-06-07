from globals import memory
from enums import InstructionPointerJump
import raava.common
from raava.memory import get_address


def execute_conditionals_cycles(quadruple):
    """Execute the instruction pointers from the quadruples in conditionals."""
    operator = quadruple[0]
    if(operator == InstructionPointerJump.GOTOF):
        execute_goto_F(quadruple)

    if(operator == InstructionPointerJump.GOTO):
        execute_goto(quadruple)


def execute_goto_F(quadruple):
    """In case the expression is false, update the instruction pointer."""
    _, adress_01, jump_to = quadruple
    adress_01 = get_address(adress_01)
    if(not memory[adress_01]):
        raava.common.instruction_pointer = jump_to - 1


def execute_goto(quadruple):
    """Update the instruction pointer to the defined jump."""
    _, jump_to = quadruple
    raava.common.instruction_pointer = jump_to - 1
