import copy
import globals
from enums import DataTypes, MemorySegments
from typing import Union


primitive_types = set(type.value for type in DataTypes)


def get_segment_size(memory_segment: dict) -> int:
    """Given a segment of the RESERVED MEMORY, calculate the size"""
    total_size = 0
    if isinstance(memory_segment, int):
        return memory_segment
    for key in memory_segment:
        segment_size = memory_segment[key]
        if isinstance(segment_size, dict):
            segment_size = get_segment_size(segment_size)
        total_size += segment_size
    return total_size


PRIMITIVE_SIZE = 500
TEMPORAL_SIZE = 250
CONSTANTS_SIZE = 250

DS_SIZES = {
    MemorySegments.DATA: 500,
    MemorySegments.TEMPORAL: 250,
    MemorySegments.CONSTANTS: 250,
}


RESERVED_MEMORY = {
    MemorySegments.DATA: {
        DataTypes.INT: {
            MemorySegments.DATA: PRIMITIVE_SIZE,
            MemorySegments.TEMPORAL: TEMPORAL_SIZE,
            MemorySegments.CONSTANTS: CONSTANTS_SIZE,
        },
        DataTypes.FLOAT: {
            MemorySegments.DATA: PRIMITIVE_SIZE,
            MemorySegments.TEMPORAL: TEMPORAL_SIZE,
            MemorySegments.CONSTANTS: CONSTANTS_SIZE,
        },
        DataTypes.BOOL: {
            MemorySegments.DATA: PRIMITIVE_SIZE,
            MemorySegments.TEMPORAL: TEMPORAL_SIZE,
            MemorySegments.CONSTANTS: CONSTANTS_SIZE,
        },
        DataTypes.CHAR: {
            MemorySegments.DATA: PRIMITIVE_SIZE,
            MemorySegments.TEMPORAL: TEMPORAL_SIZE,
            MemorySegments.CONSTANTS: CONSTANTS_SIZE,
        },
        DataTypes.CLASS: 1000,
    },
    MemorySegments.CODE: 1000,
    MemorySegments.STACK: 1000,
    MemorySegments.EXTRA: 1000,
}

# Data Segment section of the memory
DS_START_POSITION = 1000
DS_RESERVED_MEMORY = RESERVED_MEMORY[MemorySegments.DATA]

# Start positions
INT_START_POSITION = DS_START_POSITION
FLOAT_START_POSITION = INT_START_POSITION + \
    get_segment_size(DS_RESERVED_MEMORY[DataTypes.INT])
BOOL_START_POSITION = FLOAT_START_POSITION + \
    get_segment_size(DS_RESERVED_MEMORY[DataTypes.FLOAT])
CHAR_START_POSITION = BOOL_START_POSITION + \
    get_segment_size(DS_RESERVED_MEMORY[DataTypes.BOOL])
CLASS_START_POSITION = CHAR_START_POSITION + \
    get_segment_size(DS_RESERVED_MEMORY[DataTypes.CHAR])

# Code Segment section of the memory
CS_START_POSITION = 7000
assert(CS_START_POSITION >= DS_START_POSITION +
       get_segment_size(RESERVED_MEMORY[MemorySegments.DATA]))

# Stack Segment section of the memory
SS_START_POSITION = 8000
assert(SS_START_POSITION >= CS_START_POSITION +
       get_segment_size(RESERVED_MEMORY[MemorySegments.CODE]))

# ES section of the memory
ES_START_POSITION = 9000
assert(ES_START_POSITION >= SS_START_POSITION +
       get_segment_size(RESERVED_MEMORY[MemorySegments.STACK]))

START_POSITIONS = {
    MemorySegments.DATA: {
        DataTypes.INT: {
            MemorySegments.DATA: INT_START_POSITION,
            MemorySegments.TEMPORAL: INT_START_POSITION + PRIMITIVE_SIZE,
            MemorySegments.CONSTANTS: INT_START_POSITION + PRIMITIVE_SIZE + TEMPORAL_SIZE,
        },
        DataTypes.FLOAT: {
            MemorySegments.DATA: FLOAT_START_POSITION,
            MemorySegments.TEMPORAL: FLOAT_START_POSITION + PRIMITIVE_SIZE,
            MemorySegments.CONSTANTS: FLOAT_START_POSITION + PRIMITIVE_SIZE + TEMPORAL_SIZE,
        },
        DataTypes.BOOL: {
            MemorySegments.DATA: BOOL_START_POSITION,
            MemorySegments.TEMPORAL: BOOL_START_POSITION + PRIMITIVE_SIZE,
            MemorySegments.CONSTANTS: BOOL_START_POSITION + PRIMITIVE_SIZE + TEMPORAL_SIZE,
        },
        DataTypes.CHAR: {
            MemorySegments.DATA: CHAR_START_POSITION,
            MemorySegments.TEMPORAL: CHAR_START_POSITION + PRIMITIVE_SIZE,
            MemorySegments.CONSTANTS: CHAR_START_POSITION + PRIMITIVE_SIZE + TEMPORAL_SIZE,
        },
        DataTypes.CLASS: CLASS_START_POSITION,
    },
    MemorySegments.CODE: CS_START_POSITION,
    MemorySegments.STACK: SS_START_POSITION,
    MemorySegments.EXTRA: ES_START_POSITION,
}


# Counters for data types and memory segments
counters = copy.deepcopy(START_POSITIONS)
data_segment = counters[MemorySegments.DATA]


def check_ds_memory_availability(
        var_type: DataTypes, segment: MemorySegments = None):
    """Checks that the specified Data Memory segment still has enough space for
    adding another address and raises an error if not.
    """
    if segment is None:
        assert(var_type == DataTypes.CLASS)
        counter = counters[MemorySegments.DATA][var_type]
        start_position = START_POSITIONS[MemorySegments.DATA][var_type]
        memory_avilable = RESERVED_MEMORY[MemorySegments.DATA][var_type]
        if counter >= start_position + memory_avilable:
            raise Exception("Memory is full")
        return

    counter = counters[MemorySegments.DATA][var_type][segment]
    start_position = START_POSITIONS[MemorySegments.DATA][var_type][segment]
    memory_avilable = RESERVED_MEMORY[MemorySegments.DATA][var_type][segment]
    if counter >= start_position + memory_avilable:
        raise Exception("Memory is full")


def assign_into_data_segment(
        var_type: DataTypes, segment: MemorySegments = None) -> int:
    """Based on the data type and segment, allocates a space in data stack memory.
    \nReturns the resulting memory address.
    """
    check_ds_memory_availability(var_type, segment)

    if segment is None:
        assert(var_type == DataTypes.CLASS)
        memory_address = data_segment[var_type]
        data_segment[var_type] += 1
        return memory_address

    memory_address = data_segment[var_type][segment]
    data_segment[var_type][segment] += 1
    return memory_address


def assign_primitive_to_memory(var_type: DataTypes) -> int:
    """Based on the data type, allocates a space in data stack memory.
    \nReturns the resulting memory address.
    """
    return assign_into_data_segment(var_type, MemorySegments.DATA)


def assign_instance_to_memory() -> int:
    """
    Based on the data type, allocates a space in data stack memory. \n
    Returns the resulting memory address.
    """
    return assign_into_data_segment(DataTypes.CLASS)


def assign_temporal(var_type: DataTypes) -> int:
    """Based on the data type, allocates a space in data stack memory. \n
    Returns the resulting memory address.
    """
    return assign_into_data_segment(var_type, MemorySegments.TEMPORAL)


def assign_constant(
        value: Union[bool, int, float, str],
        var_type: DataTypes = None) -> int:
    """Based on the data type, allocates a space in data stack memory. \n
    Returns the resulting memory address.
    """
    address = None
    if var_type is None:
        address = assign_into_extra_segment()
    else:
        address = assign_into_data_segment(var_type, MemorySegments.CONSTANTS)
    globals.memory[address] = value
    return address


def get_type_by_address(address: int) -> DataTypes:
    """
    Based on a memory address from the Data segment, return the Data Type. \n
    If given address is not in range for an int, float, char or bool, raises an
    exception.
    """
    if not in_data_segment(address):
        raise Exception("")

    if address >= CLASS_START_POSITION:
        return DataTypes.CLASS
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


def is_class(address) -> bool:
    CLASS_END_POSITION = CLASS_START_POSITION + \
        get_segment_size(DS_RESERVED_MEMORY[DataTypes.CHAR])
    if address >= CLASS_START_POSITION and address < CLASS_END_POSITION:
        return True
    return False


def in_data_segment(address) -> bool:
    data_segment_size = get_segment_size(RESERVED_MEMORY[MemorySegments.DATA])
    DS_END_POSITION = DS_START_POSITION + data_segment_size
    in_data_segment = address >= DS_START_POSITION and address < DS_END_POSITION
    return in_data_segment


def is_primitive(address: int) -> bool:
    address_type = get_type_by_address(address)
    if address_type.value in primitive_types:
        return True
    return False


def is_temporal(address: int) -> bool:
    if not in_data_segment(address):
        raise Exception("Not in Data Segment.")
    if not is_primitive(address):
        raise Exception("Not a primitive value.")
    position_in_segment = address % 1000
    return position_in_segment >= PRIMITIVE_SIZE and position_in_segment < PRIMITIVE_SIZE + TEMPORAL_SIZE
