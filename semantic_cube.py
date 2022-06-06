from enums import DataTypes, Operators


type_error = ValueError("Type mismatch")


semantic_cube = {
    Operators.ADD: {
        DataTypes.INT: {
            DataTypes.INT: DataTypes.INT,
            DataTypes.FLOAT: DataTypes.FLOAT,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.FLOAT: {
            DataTypes.INT: DataTypes.FLOAT,
            DataTypes.FLOAT: DataTypes.FLOAT,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.CHAR: {
            DataTypes.INT: type_error,
            DataTypes.FLOAT: type_error,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.BOOL: {
            DataTypes.INT: type_error,
            DataTypes.FLOAT: type_error,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        }
    },
    Operators.MINUS: {
        DataTypes.INT: {
            DataTypes.INT: DataTypes.INT,
            DataTypes.FLOAT: DataTypes.FLOAT,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.FLOAT: {
            DataTypes.INT: DataTypes.FLOAT,
            DataTypes.FLOAT: DataTypes.FLOAT,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.CHAR: {
            DataTypes.INT: type_error,
            DataTypes.FLOAT: type_error,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.BOOL: {
            DataTypes.INT: type_error,
            DataTypes.FLOAT: type_error,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        }
    },
    Operators.MULTIPLY: {
        DataTypes.INT: {
            DataTypes.INT: DataTypes.INT,
            DataTypes.FLOAT: DataTypes.FLOAT,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.FLOAT: {
            DataTypes.INT: DataTypes.FLOAT,
            DataTypes.FLOAT: DataTypes.FLOAT,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.CHAR: {
            DataTypes.INT: type_error,
            DataTypes.FLOAT: type_error,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.BOOL: {
            DataTypes.INT: type_error,
            DataTypes.FLOAT: type_error,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        }
    },
    Operators.DIVIDE: {
        DataTypes.INT: {
            DataTypes.INT: DataTypes.INT,
            DataTypes.FLOAT: DataTypes.FLOAT,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.FLOAT: {
            DataTypes.INT: DataTypes.FLOAT,
            DataTypes.FLOAT: DataTypes.FLOAT,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.CHAR: {
            DataTypes.INT: type_error,
            DataTypes.FLOAT: type_error,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.BOOL: {
            DataTypes.INT: type_error,
            DataTypes.FLOAT: type_error,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        }
    },
    Operators.REL_OP_GT: {
        DataTypes.INT: {
            DataTypes.INT: DataTypes.BOOL,
            DataTypes.FLOAT: DataTypes.BOOL,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.FLOAT: {
            DataTypes.INT: DataTypes.BOOL,
            DataTypes.FLOAT: DataTypes.BOOL,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.CHAR: {
            DataTypes.INT: type_error,
            DataTypes.FLOAT: type_error,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.BOOL: {
            DataTypes.INT: type_error,
            DataTypes.FLOAT: type_error,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        }
    },
    Operators.REL_OP_LT: {
        DataTypes.INT: {
            DataTypes.INT: DataTypes.BOOL,
            DataTypes.FLOAT: DataTypes.BOOL,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.FLOAT: {
            DataTypes.INT: DataTypes.BOOL,
            DataTypes.FLOAT: DataTypes.BOOL,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.CHAR: {
            DataTypes.INT: type_error,
            DataTypes.FLOAT: type_error,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.BOOL: {
            DataTypes.INT: type_error,
            DataTypes.FLOAT: type_error,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        }
    },
    Operators.REL_OP_NE: {
        DataTypes.INT: {
            DataTypes.INT: DataTypes.BOOL,
            DataTypes.FLOAT: DataTypes.BOOL,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.FLOAT: {
            DataTypes.INT: DataTypes.BOOL,
            DataTypes.FLOAT: DataTypes.BOOL,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.CHAR: {
            DataTypes.INT: type_error,
            DataTypes.FLOAT: type_error,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: DataTypes.BOOL
        },
        DataTypes.BOOL: {
            DataTypes.INT: type_error,
            DataTypes.FLOAT: type_error,
            DataTypes.BOOL: DataTypes.BOOL,
            DataTypes.CHAR: type_error
        }
    },
    Operators.REL_OP_EQ: {
        DataTypes.INT: {
            DataTypes.INT: DataTypes.BOOL,
            DataTypes.FLOAT: DataTypes.BOOL,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.FLOAT: {
            DataTypes.INT: DataTypes.BOOL,
            DataTypes.FLOAT: DataTypes.BOOL,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: type_error
        },
        DataTypes.CHAR: {
            DataTypes.INT: type_error,
            DataTypes.FLOAT: type_error,
            DataTypes.BOOL: type_error,
            DataTypes.CHAR: DataTypes.BOOL
        },
        DataTypes.BOOL: {
            DataTypes.INT: type_error,
            DataTypes.FLOAT: type_error,
            DataTypes.BOOL: DataTypes.BOOL,
            DataTypes.CHAR: type_error
        }
    }
}
