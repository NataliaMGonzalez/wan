from typing import Tuple
from enums import ArrayOperations


import globals

memory = globals.memory


def execute_array(quadruple: Tuple[ArrayOperations, int, int, int]):
    _, base_address, exp_address, new_address = quadruple
    offset = memory[exp_address]
    value = memory[base_address + offset]
    memory[new_address] = value
