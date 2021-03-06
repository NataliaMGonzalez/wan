from typing import Any
import globals
from addresses_manager import (
    CS_START_POSITION, RESERVED_MEMORY, SS_START_POSITION, counters)
from enums import MemorySegments


# When entering into a function, this stack will keep the previous values
FUNCTION_STACK_RESERVED_MEMORY = RESERVED_MEMORY[MemorySegments.STACK]

# When going into a function, save the current instruction to be executed
INSTRUCTIONS_STACK_RESERVED_MEMORY = RESERVED_MEMORY[MemorySegments.CODE]


def check_function_stack_availability():
    """Raises an exeption if the function stack is full."""
    counter = counters[MemorySegments.STACK]
    start_position = SS_START_POSITION
    memory_avilable = FUNCTION_STACK_RESERVED_MEMORY
    if counter >= start_position + memory_avilable:
        raise Exception("Stack overflow.")


def assign_into_function_stack(value):
    """Places a value from the memory into the function stack."""
    check_function_stack_availability()
    memory_address = counters[MemorySegments.STACK]
    globals.memory[memory_address] = value
    counters[MemorySegments.STACK] += 1


def retreive_from_function_stack() -> Any:
    """Retreives a value from the function stack to be loaded again in memory."""
    counter = counters[MemorySegments.STACK]
    if counter < SS_START_POSITION:
        raise Exception("Error un function handling.")
    memory_address = counters[MemorySegments.STACK] - 1
    value = globals.memory[memory_address]
    counters[MemorySegments.STACK] -= 1
    return value


def check_code_stack_availability():
    """Raises an exeption if the code stack is full."""
    counter = counters[MemorySegments.CODE]
    start_position = CS_START_POSITION
    memory_avilable = INSTRUCTIONS_STACK_RESERVED_MEMORY
    if counter >= start_position + memory_avilable:
        raise Exception("Maximum recursion limit exceeded.")


def assign_into_code_stack(value):
    """Places a value from the memory into the code stack."""
    check_code_stack_availability()
    memory_address = counters[MemorySegments.CODE]
    globals.memory[memory_address] = value
    counters[MemorySegments.CODE] += 1


def retreive_from_code_stack() -> int:
    """Retreives the instruction pointer from the code stack to be loaded again in memory."""
    counter = counters[MemorySegments.CODE]
    if counter < CS_START_POSITION:
        raise Exception("Error on code stack handling.")
    memory_address = counters[MemorySegments.CODE] - 1
    value = globals.memory[memory_address]
    counters[MemorySegments.CODE] -= 1
    return value


def get_address(address) -> int:
    """Recursively traverse into the pointers until finding a direct value."""
    memory = globals.memory
    if address not in memory:
        return address
    value = memory[address]
    if not isinstance(memory[address], tuple):
        return address
    return get_address(value[0])
