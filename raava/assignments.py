from typing import Tuple
from addresses_manager import CLASS_START_POSITION, DS_RESERVED_MEMORY, get_segment_size
from enums import DataTypes, Operators
import globals
from raava.memory import get_address


memory = globals.memory


def execute_assignment(quadruple: Tuple[Operators, int, int, int]):
    """ Executes the instruction that assigns one address to another. """
    _, new_address, original_address = quadruple
    new_address = get_address(new_address)
    original_address = get_address(original_address)
    if is_class(new_address) and is_class(original_address):
        memory[new_address] = (original_address,)
        return
    memory[new_address] = memory[original_address]


def is_class(address):
    CLASS_END_POSITION = CLASS_START_POSITION + \
        get_segment_size(DS_RESERVED_MEMORY[DataTypes.CHAR])
    if address >= CLASS_START_POSITION and address < CLASS_END_POSITION:
        return True
    return False
