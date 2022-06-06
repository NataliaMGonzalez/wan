from lark import Tree
from enums import DataTypes, Operators
from addresses_manager import assign_temporal, get_type_by_address
from semantic_cube import semantic_cube


def check_operations(
        operation: Operators, address_01: int, address_02: int) -> DataTypes:
    """Raises an exception if the two variable types from the addresses are not
    compatible for the specified operation.
    """
    type_01 = get_type_by_address(address_01)
    type_02 = get_type_by_address(address_02)
    result_type = semantic_cube[operation][type_01][type_02]
    if isinstance(operation, Exception):
        raise result_type
    return result_type


def add_operation_quadruple(self, operator: Operators):
    """Gets the two last addresses in the stack and adds the corresponding
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
    operator = Operators(tree.children[1].value)
    add_operation_quadruple(self, operator)


def and_expression(self, tree):
    operator = Operators(tree.children[1].value)
    add_operation_quadruple(self, operator)


def not_expression(self, _tree: Tree):
    operand = self.addresses_stack.pop()
    address = assign_temporal(DataTypes.BOOL)
    quad = (Operators.NOT, operand, address)
    self.quadruples.append(quad)
    self.addresses_stack.append(address)


def comp_expression(self, tree):
    operator = Operators(tree.children[1].value)
    add_operation_quadruple(self, operator)


def sum_expression(self, tree):
    operator = Operators(tree.children[1].value)
    add_operation_quadruple(self, operator)


def term(self, tree):
    operator = Operators(tree.children[1].value)
    add_operation_quadruple(self, operator)
