from enum import Enum


class DataTypes(Enum):
    BOOL = "bool"
    INT = "int"
    FLOAT = "float"
    CHAR = "char"


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
    LOG_OP_NOT = "!"
