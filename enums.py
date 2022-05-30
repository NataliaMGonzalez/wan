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


class AssignmentOperators(Enum):
    ASSIGN = "="


class Operators(Enum):
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


class InputOutputInstructions(Enum):
    READ = "READ"
    WRITE = "PRINT"


class FunctionOperators(Enum):
    GOSUB = "GOSUB"
    ERA = "ERA"
    RETURN = "RETURN"
    PUSH_IN_STACK = "PUSH_STACK"
    PULL_FROM_STACK = "PULL_FROM_STACK"
    SAVE_PARAM = "SAVE_PARAM"


class ArrayOperations(Enum):
    POINT_TO = "point_to"
