from globals import memory
from typing import Tuple
from enums import ArrayOperations
from raava.memory import get_address


def execute_array(quadruple: Tuple[ArrayOperations, int, int, int]):
    _, base_address, exp_address, new_address = quadruple
    base_address = get_address(base_address)
    exp_address = get_address(exp_address)
    offset = memory[exp_address]
    value = memory[base_address + offset]
    memory[new_address] = value
