from enums import DataTypes, MemorySegments


RESERVED_MEMORY = {
    MemorySegments.DATA: {
        DataTypes.INT: 1000,
        DataTypes.FLOAT: 1000,
        DataTypes.BOOL: 1000,
        DataTypes.CHAR: 1000,
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

# Code Segment section of the memory
CS_START_POSITION = 5000
assert(CS_START_POSITION >= CHAR_START_POSITION +
       RESERVED_MEMORY[MemorySegments.DATA][DataTypes.CHAR])

# Stack Segment section of the memory
SS_START_POSITION = 8000
assert(SS_START_POSITION >= CHAR_START_POSITION +
       RESERVED_MEMORY[MemorySegments.CODE])

# ES section of the memory
ES_START_POSITION = 9000
assert(ES_START_POSITION >= SS_START_POSITION +
       RESERVED_MEMORY[MemorySegments.STACK])

DS_START_POSITIONS = {
    DataTypes.INT: INT_START_POSITION,
    DataTypes.FLOAT: FLOAT_START_POSITION,
    DataTypes.BOOL: BOOL_START_POSITION,
    DataTypes.CHAR: CHAR_START_POSITION,
}

memory = {}

counters = {
    DataTypes.INT: INT_START_POSITION,
    DataTypes.FLOAT: FLOAT_START_POSITION,
    DataTypes.BOOL: BOOL_START_POSITION,
    DataTypes.CHAR: CHAR_START_POSITION
}


def check_memory_availability(var_type):
    counter = counters[var_type]
    start_position = DS_START_POSITIONS[var_type]
    memory_avilable = DS_RESERVED_MEM[var_type]
    if counter >= start_position + memory_avilable:
        raise Exception("Memory is full")


def assign_to_memory(var_type, value):
    check_memory_availability(var_type)
    memory_address = counters[var_type]
    memory[memory_address] = value
    counters[var_type] += 1
    return memory_address


def get_type_by_address(address):
    if address > CHAR_START_POSITION + DS_RESERVED_MEM[DataTypes.CHAR]:
        return "Not a variable."
    if address >= CHAR_START_POSITION:
        return DataTypes.CHAR
    if address >= BOOL_START_POSITION:
        return DataTypes.BOOL
    if address >= FLOAT_START_POSITION:
        return DataTypes.FLOAT
    if address >= INT_START_POSITION:
        return DataTypes.INT
    return "Not a variable."
