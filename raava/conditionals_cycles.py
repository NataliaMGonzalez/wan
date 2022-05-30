from ast import operator
from typing import Tuple
from enums import InstructionPointerJump
import raava.common

import globals

memory = globals.memory


def execute_conditionals_cycles(quadruple):
    operator = quadruple[0]
    if(operator == InstructionPointerJump.GOTOF):
        _, adress_01, jump_to = quadruple

        if(not memory[adress_01]):
            raava.common.instruction_pointer = jump_to - 1

    if(operator == InstructionPointerJump.GOTO):
        _, jump_to = quadruple
        raava.common.instruction_pointer = jump_to - 1
