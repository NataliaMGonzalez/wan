from typing import Tuple
from addresses_manager import is_class
from enums import Operators
import globals
from raava.memory import get_address


memory = globals.memory


def execute_assignment(quadruple: Tuple[Operators, int, int, int]):
    """Executes the instruction that assigns one address to another.

    Modify the memory in the first (new) address and set to it the value located
    in the original address. In case the addresses are classes, in the new
    address create a pointer to the original address.
    """
    _, new_address, original_address = quadruple
    new_address = get_address(new_address)
    original_address = get_address(original_address)
    if is_class(new_address) and is_class(original_address):
        memory[new_address] = (original_address,)
        return
    memory[new_address] = memory[original_address]
