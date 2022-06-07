from lark import Tree
from enums import DataTypes, Operators
from addresses_manager import assign_temporal, get_type_by_address
from semantic_cube import semantic_cube


def check_operations(
        operation: Operators, address_01: int, address_02: int) -> DataTypes:
    """Checks the compatibility of the addresses types.

    Raises an exception if the two variable types from the addresses are not
    compatible for the specified operation.
    """
    type_01 = get_type_by_address(address_01)
    type_02 = get_type_by_address(address_02)
    result_type = semantic_cube[operation][type_01][type_02]
    if isinstance(operation, Exception):
        raise result_type
    return result_type


def add_binary_operation_quadruple(self, operator: Operators):
    """Create quadruple for the operation between the last two expressions.

    Gets the two last addresses in the stack and adds the corresponding
    operation quadruple into the list. Checks for the type compatibility first.
    """
    right_operand = self.addresses_stack.pop()
    left_operand = self.addresses_stack.pop()
    result_type = check_operations(operator, left_operand, right_operand)
    address = assign_temporal(result_type)
    quad = (operator, left_operand, right_operand, address)
    self.quadruples.append(quad)
    self.addresses_stack.append(address)


def or_expression(self, tree):
    """OR operation expression.

    `or_expression: and_expression (BOOL_OP_OR and_expression)?`
    """
    operator = Operators(tree.children[1].value)
    add_binary_operation_quadruple(self, operator)


def and_expression(self, tree):
    """AND operation expression.

    `and_expression: not_expression (BOOL_OP_AND not_expression)?`
    """
    operator = Operators(tree.children[1].value)
    add_binary_operation_quadruple(self, operator)


def not_expression(self, _tree: Tree):
    """NOT unary operation expression.

    `not_expression: (NOT)? comp_expression`
    """
    operand = self.addresses_stack.pop()
    address = assign_temporal(DataTypes.BOOL)
    quad = (Operators.NOT, operand, address)
    self.quadruples.append(quad)
    self.addresses_stack.append(address)


def comp_expression(self, tree):
    """Arithmetic comparisons expressions.

    `comp_expression: sum_expression (relop sum_expression)?`
    """
    operator = Operators(tree.children[1].value)
    add_binary_operation_quadruple(self, operator)


def sum_expression(self, tree):
    """Sum operation expression.

    `sum_expression: (sum_expression (ARIT_OPS_SUBTRACT | ARIT_OPS_SUM))? term`
    """
    operator = Operators(tree.children[1].value)
    add_binary_operation_quadruple(self, operator)


def term(self, tree):
    """Multiplication operation expression.

    `term: (term (ARIT_OPS_DIVIDE | ARIT_OPS_MULTIPLY))? factor`
    """
    operator = Operators(tree.children[1].value)
    add_binary_operation_quadruple(self, operator)
