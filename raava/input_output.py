from typing import Tuple
from enums import InputOutputInstructions
import globals
from raava.memory import get_address


memory = globals.memory


def execute_input_output(quadruple: Tuple[InputOutputInstructions, int]):
    instruction, address = quadruple
    address = get_address(address)
    if (instruction == InputOutputInstructions.WRITE):
        print(memory[address], " ")
    if (instruction == InputOutputInstructions.READ):
        memory[address] = input(">> ")
