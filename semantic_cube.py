from enums import DataTypes, Operators

def error_function(_x = None, _y = None):
    raise ValueError("Type mismatch")


semantic_cube = {
    Operators.ADD: {
        DataTypes.INT: {
            DataTypes.INT: DataTypes.INT,
            DataTypes.FLOAT: DataTypes.FLOAT,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: DataTypes.FLOAT,
            DataTypes.FLOAT: DataTypes.FLOAT,
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
            DataTypes.INT: DataTypes.INT,
            DataTypes.FLOAT: DataTypes.FLOAT,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: DataTypes.FLOAT,
            DataTypes.FLOAT: DataTypes.FLOAT,
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
            DataTypes.INT: DataTypes.INT,
            DataTypes.FLOAT: DataTypes.FLOAT,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: DataTypes.FLOAT,
            DataTypes.FLOAT: DataTypes.FLOAT,
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
            DataTypes.INT: DataTypes.FLOAT,
            DataTypes.FLOAT: DataTypes.FLOAT,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: DataTypes.FLOAT,
            DataTypes.FLOAT: DataTypes.FLOAT,
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
            DataTypes.INT: DataTypes.BOOL,
            DataTypes.FLOAT: DataTypes.BOOL,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: DataTypes.BOOL,
            DataTypes.FLOAT: DataTypes.BOOL,
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
            DataTypes.INT: DataTypes.BOOL,
            DataTypes.FLOAT: DataTypes.BOOL,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: DataTypes.BOOL,
            DataTypes.FLOAT: DataTypes.BOOL,
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
            DataTypes.INT: DataTypes.BOOL,
            DataTypes.FLOAT: DataTypes.BOOL,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: DataTypes.BOOL,
            DataTypes.FLOAT: DataTypes.BOOL,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.CHAR: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: DataTypes.BOOL
        },
        DataTypes.BOOL: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: DataTypes.BOOL,
            DataTypes.CHAR: error_function
        }
    },
    Operators.REL_OP_EQ: {
        DataTypes.INT: {
            DataTypes.INT: DataTypes.BOOL,
            DataTypes.FLOAT: DataTypes.BOOL,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: DataTypes.BOOL,
            DataTypes.FLOAT: DataTypes.BOOL,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.CHAR: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: DataTypes.BOOL
        },
        DataTypes.BOOL: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: DataTypes.BOOL,
            DataTypes.CHAR: error_function
        }
    },
    Operators.LOG_OP_AND: {
        DataTypes.INT: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
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
            DataTypes.BOOL: DataTypes.BOOL,
            DataTypes.CHAR: error_function
        }
    },
    Operators.LOG_OP_OR: {
        DataTypes.INT: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
            DataTypes.BOOL: error_function,
            DataTypes.CHAR: error_function
        },
        DataTypes.FLOAT: {
            DataTypes.INT: error_function,
            DataTypes.FLOAT: error_function,
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
            DataTypes.BOOL: DataTypes.BOOL,
            DataTypes.CHAR: error_function
        }
    },
    Operators.LOG_OP_NOT: {
        DataTypes.INT: error_function,
        DataTypes.FLOAT: error_function,
        DataTypes.CHAR: error_function,
        DataTypes.BOOL: DataTypes.BOOL
    }
}