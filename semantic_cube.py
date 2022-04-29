from enums import DataTypes, Operators


def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    return x / y


def rel_op_gt(x, y):
    return x > y


def rel_op_lt(x, y):
    return x < y


def rel_op_ne(x, y):
    return x != y


def rel_op_eq(x, y):
    return x == y


def error_function(_x, _y):
    raise ValueError("Type mismatch")


semantic_cube = {
    Operators.ADD: {
        DataTypes.INT: {
            DataTypes.INT: add,
            DataTypes.FLOAT: add,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: add,
            DataTypes.FLOAT: add,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.CHAR: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.BOOL: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        }
    },
    Operators.MINUS: {
        DataTypes.INT: {
            DataTypes.INT: subtract,
            DataTypes.FLOAT: subtract,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: subtract,
            DataTypes.FLOAT: subtract,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.CHAR: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.BOOL: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        }
    },
    Operators.MULTIPLY: {
        DataTypes.INT: {
            DataTypes.INT: multiply,
            DataTypes.FLOAT: multiply,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: multiply,
            DataTypes.FLOAT: multiply,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.CHAR: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.BOOL: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        }
    },
    Operators.DIVIDE: {
        DataTypes.INT: {
            DataTypes.INT: divide,
            DataTypes.FLOAT: divide,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: divide,
            DataTypes.FLOAT: divide,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.CHAR: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.BOOL: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        }
    },
    Operators.REL_OP_GT: {
        DataTypes.INT: {
            DataTypes.INT: rel_op_gt,
            DataTypes.FLOAT: rel_op_gt,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: rel_op_gt,
            DataTypes.FLOAT: rel_op_gt,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.CHAR: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.BOOL: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        }
    },
    Operators.REL_OP_LT: {
        DataTypes.INT: {
            DataTypes.INT: rel_op_lt,
            DataTypes.FLOAT: rel_op_lt,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: rel_op_lt,
            DataTypes.FLOAT: rel_op_lt,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.CHAR: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.BOOL: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        }
    },
    Operators.REL_OP_NE: {
        DataTypes.INT: {
            DataTypes.INT: rel_op_ne,
            DataTypes.FLOAT: rel_op_ne,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: rel_op_ne,
            DataTypes.FLOAT: rel_op_ne,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.CHAR: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: rel_op_ne
        },
        DataTypes.BOOL: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: rel_op_ne,
            DataTypes.CHAR: error_function
        }
    },
    Operators.REL_OP_EQ: {
        DataTypes.INT: {
            DataTypes.INT: rel_op_eq,
            DataTypes.FLOAT: rel_op_eq,
            DataTypes.BOOL: rel_op_eq,
            DataTypes.CHAR: rel_op_eq
        },
        DataTypes.FLOAT: {
            DataTypes.INT: rel_op_eq,
            DataTypes.FLOAT: rel_op_eq,
            DataTypes.BOOL: rel_op_eq,
            DataTypes.CHAR: rel_op_eq
        },
        DataTypes.CHAR: {
            DataTypes.INT: rel_op_eq,
            DataTypes.FLOAT: rel_op_eq,
            DataTypes.BOOL: rel_op_eq,
            DataTypes.CHAR: rel_op_eq
        },
        DataTypes.BOOL: {
            DataTypes.INT: rel_op_eq,
            DataTypes.FLOAT: rel_op_eq,
            DataTypes.BOOL: rel_op_eq,
            DataTypes.CHAR: rel_op_eq
        }
    }
}
