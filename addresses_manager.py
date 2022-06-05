import globals
import re
from enums import DataTypes, MemorySegments
from typing import Union
from utils import str_to_bool


RESERVED_MEMORY = {
    MemorySegments.DATA: {
        DataTypes.INT: 1000,
        DataTypes.FLOAT: 1000,
        DataTypes.BOOL: 1000,
        DataTypes.CHAR: 1000,
        DataTypes.CLASS: 1000,
    },
    MemorySegments.CODE: 1000,
    MemorySegments.STACK: 1000,
    MemorySegments.EXTRA: 1000
}

# Data Segment section of the memory
DS_START_POSITION = 1000
DS_RESERVED_MEM = RESERVED_MEMORY[MemorySegments.DATA]

INT_START_POSITION = DS_START_POSITION
FLOAT_START_POSITION = INT_START_POSITION + DS_RESERVED_MEM[DataTypes.INT]
BOOL_START_POSITION = FLOAT_START_POSITION + DS_RESERVED_MEM[DataTypes.FLOAT]
CHAR_START_POSITION = BOOL_START_POSITION + DS_RESERVED_MEM[DataTypes.BOOL]
CLASS_START_POSITION = CHAR_START_POSITION + DS_RESERVED_MEM[DataTypes.CHAR]

DS_START_POSITIONS = {
    DataTypes.INT: INT_START_POSITION,
    DataTypes.FLOAT: FLOAT_START_POSITION,
    DataTypes.BOOL: BOOL_START_POSITION,
    DataTypes.CHAR: CHAR_START_POSITION,
    DataTypes.CLASS: CLASS_START_POSITION,
}

# Code Segment section of the memory
CS_START_POSITION = 7000
assert(CS_START_POSITION >= CLASS_START_POSITION +
       RESERVED_MEMORY[MemorySegments.DATA][DataTypes.CLASS])

# Stack Segment section of the memory
SS_START_POSITION = 8000
assert(SS_START_POSITION >= CS_START_POSITION +
       RESERVED_MEMORY[MemorySegments.CODE])

# ES section of the memory
ES_START_POSITION = 9000
assert(ES_START_POSITION >= SS_START_POSITION +
       RESERVED_MEMORY[MemorySegments.STACK])


# Counters for data types and memory segments
counters = {
    DataTypes.INT: INT_START_POSITION,
    DataTypes.FLOAT: FLOAT_START_POSITION,
    DataTypes.BOOL: BOOL_START_POSITION,
    DataTypes.CHAR: CHAR_START_POSITION,
    DataTypes.CLASS: CLASS_START_POSITION,
    MemorySegments.CODE: CS_START_POSITION,
    MemorySegments.STACK: SS_START_POSITION,
    MemorySegments.EXTRA: ES_START_POSITION,
}


def check_ds_memory_availability(var_type: DataTypes):
    """
    Checks that the Data Memory segment still has enough space for adding
    another address and raises an error if not.
    """
    counter = counters[var_type]
    start_position = DS_START_POSITIONS[var_type]
    memory_avilable = DS_RESERVED_MEM[var_type]
    if counter >= start_position + memory_avilable:
        raise Exception("Memory is full")


def assign_primitive_to_memory(var_type: DataTypes) -> int:
    """
    Based on the data type, allocates a space in data stack memory. \n
    Returns the resulting memory address.
    """
    check_ds_memory_availability(var_type)
    memory_address = counters[var_type]
    counters[var_type] += 1
    return memory_address


def assign_instance_to_memory() -> int:
    """
    Based on the data type, allocates a space in data stack memory. \n
    Returns the resulting memory address.
    """
    class_type = DataTypes.CLASS
    check_ds_memory_availability(class_type)
    memory_address = counters[class_type]
    counters[class_type] += 1
    return memory_address


def get_type_by_address(address: int) -> DataTypes:
    """
    Based on a memory address from the Data segment, return the Data Type. \n
    If given address is not in range for an int, float, char or bool, raises an
    exception.
    """
    DS_END_POSITION = CHAR_START_POSITION + DS_RESERVED_MEM[DataTypes.CHAR]
    not_a_data_segment_address = address < DS_START_POSITION or address >= DS_END_POSITION
    if not_a_data_segment_address:
        raise Exception("")

    if address >= CHAR_START_POSITION:
        return DataTypes.CHAR
    if address >= BOOL_START_POSITION:
        return DataTypes.BOOL
    if address >= FLOAT_START_POSITION:
        return DataTypes.FLOAT
    if address >= INT_START_POSITION:
        return DataTypes.INT


def check_es_memory_availability():
    """
    Checks that the Extra Memory segment still has enough space for adding
    another address and raises an error if not.
    """
    counter = counters[MemorySegments.EXTRA]
    if counter >= ES_START_POSITION + RESERVED_MEMORY[MemorySegments.EXTRA]:
        raise Exception("Memory is full")


def assign_into_extra_segment() -> int:
    """
    Allocates a space in the Extra Memory segment. \n
    Returns its new address.
    """
    check_es_memory_availability()
    memory_address = counters[MemorySegments.EXTRA]
    counters[MemorySegments.EXTRA] += 1
    return memory_address


def assign_constant(value: Union[bool, int, str]) -> int:
    """
    Allocates a space in the Extra Memory segment and assigns the value into
    the constants variable, which is used to initiate the memory on execution.
    \nReturns its new address.
    """
    memory_address = assign_into_extra_segment()
    if isinstance(value, str):
        if re.search(r"\b(true|false)\b", value) is not None:
            value = str_to_bool(value)
        elif re.search(r"^[0-9]+$", value) is not None:
            value = int(value)
    constants = globals.constants
    constants[memory_address] = value
    return memory_address
