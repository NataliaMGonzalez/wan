from typing import Tuple
from enums import Operators
import globals
from raava.memory import get_address


memory = globals.memory


def execute_assignment(quadruple: Tuple[Operators, int, int, int]):
    """ Executes the instruction that assigns one address to another. """
    _, new_address, original_address = quadruple
    new_address = get_address(new_address)
    original_address = get_address(original_address)
    memory[new_address] = memory[original_address]
