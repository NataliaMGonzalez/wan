from globals import memory
from typing import Tuple
from enums import ArrayOperations
from raava.memory import get_address


def execute_array(quadruple: Tuple[ArrayOperations, int, int, int]):
    instruction = quadruple[0]
    if instruction == ArrayOperations.VERIFY:
        _, exp_address, size = quadruple
        exp_address = get_address(exp_address)
        exp_result = memory[exp_address]
        if exp_result >= size:
            raise Exception("Index out of range Exception.")

    if instruction == ArrayOperations.POINT_TO:
        _, base_address, exp_address, new_address = quadruple
        base_address = get_address(base_address)
        exp_address = get_address(exp_address)
        offset = memory[exp_address]
        target_address = base_address + offset
        memory[new_address] = (target_address,)
