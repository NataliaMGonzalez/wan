from enum import Enum


class DataTypes(Enum):
    BOOL = "bool"
    INT = "int"
    FLOAT = "float"
    CHAR = "char"


class FunctionReturnTypes(Enum):
    BOOL = "bool"
    INT = "int"
    FLOAT = "float"
    CHAR = "char"
    ACTION = "action"


class Operators(Enum):
    ASSIGN = "="
    ADD = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    REL_OP_GT = ">"
    REL_OP_LT = "<"
    REL_OP_NE = "<>"
    REL_OP_EQ = "=="
    LOG_OP_AND = "&&"
    LOG_OP_OR = "||"


class MemorySegments(Enum):
    DATA = 1
    CODE = 2
    STACK = 3
    EXTRA = 4


class InstructionPointerJump(Enum):
    GOTOF = "go_to_F"
    GOTOT = "go_to_T"
    GOTO = "go_to"
