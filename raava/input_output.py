from typing import Tuple
from enums import InputOutputInstructions
import globals
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
    memory[address] = input(">> ")
