import re
from typing import Tuple, Union
from enums import InputOutputInstructions
import globals
from quadruples.constants import str_to_bool
from raava.memory import get_address


memory = globals.memory


def execute_input_output(quadruple: Tuple[InputOutputInstructions, int]):
    """Executes the quadruples for input and output, printing and inputting."""
    instruction = quadruple[0]
    if (instruction == InputOutputInstructions.WRITE):
        execute_write(quadruple)
    if (instruction == InputOutputInstructions.READ):
        execute_read(quadruple)


def execute_write(quadruple: Tuple[InputOutputInstructions, int]):
    """Executes the printing of the given address."""
    _, address = quadruple
    address = get_address(address)
    print(memory[address], " ")


def execute_read(quadruple: Tuple[InputOutputInstructions, int]):
    """Executes the inputting of the given address."""
    _, address = quadruple
    address = get_address(address)
    value: str = input(">> ")
    return_value = adapt_to_type(value)
    memory[address] = return_value


def adapt_to_type(value: str) -> Union[str, int, float, bool]:
    """Based on the string, parse to the appropriate type."""
    return_value = value
    is_int = re.search(r"^[0-9]+$", value)
    if is_int:
        return_value = int(value)
    is_float = re.search(r"^[0-9]+\.[0-9]*$", value)
    if is_float:
        return_value = float(value)
    is_bool = re.search(r"^true$|^false$", value)
    if is_bool:
        return_value = str_to_bool(value)
    return return_value
