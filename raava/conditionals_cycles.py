from globals import memory
from enums import InstructionPointerJump
import raava.common
from raava.memory import get_address


def execute_conditionals_cycles(quadruple):
    operator = quadruple[0]
    if(operator == InstructionPointerJump.GOTOF):
        _, adress_01, jump_to = quadruple
        adress_01 = get_address(adress_01)
        if(not memory[adress_01]):
            raava.common.instruction_pointer = jump_to - 1

    if(operator == InstructionPointerJump.GOTO):
        _, jump_to = quadruple
        raava.common.instruction_pointer = jump_to - 1
