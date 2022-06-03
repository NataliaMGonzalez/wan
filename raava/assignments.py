from typing import Tuple
from enums import Operators
import globals


memory = globals.memory


def execute_assignment(quadruple: Tuple[Operators, int, int, int]):
    """ Executes the instruction that assigns one address to another. """
    _, new_address, original_address = quadruple
    memory[new_address] = memory[original_address]
