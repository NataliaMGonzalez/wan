from globals import memory
from typing import Tuple
from enums import ArrayOperations
from raava.memory import get_address


def execute_array(quadruple: Tuple[ArrayOperations, int, int, int]):
    instruction, base_address, exp_address, new_address = quadruple
    base_address = get_address(base_address)
    exp_address = get_address(exp_address)

    if instruction == ArrayOperations.POINT_TO:
        offset = memory[exp_address]
        target_address = base_address + offset
        memory[new_address] = (target_address,)
