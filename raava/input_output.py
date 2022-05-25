from typing import Tuple
from enums import InputOutputInstructions
import globals


memory = globals.memory


def execute_input_output(quadruple: Tuple[InputOutputInstructions, int]):
    instruction, address = quadruple
    if (instruction == InputOutputInstructions.WRITE):
        print(memory[address])
    if (instruction == InputOutputInstructions.READ):
        memory[address] = input(">> ")
