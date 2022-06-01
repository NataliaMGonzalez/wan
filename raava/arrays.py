from ast import operator
from typing import Tuple
from enums import InstructionPointerJump
import raava.common
from enums import ArrayOperations


import globals

memory = globals.memory


def execute_array(quadruple: Tuple[ArrayOperations, int, int, int]):
    #    pointer_quad = (ArrayOperations.POINT_TO, base_address,
    #                     total_sum_address, result_address)
    _, base_address, exp_address, new_address = quadruple
    total_sum_address = memory[exp_address]
    memory[new_address] = base_address + total_sum_address
