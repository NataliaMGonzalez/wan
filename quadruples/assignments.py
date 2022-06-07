from lark import Tree
from addresses_manager import get_type_by_address, in_data_segment
from enums import AssignmentOperators


def check_operations(address_01: int, address_02: int):
    """Checks that the addresses are the same for the assignation.

    Raises an exception if the two variable types from the addresses are not
    the same type, therefore not compatible for assignation.
    """
    type_01 = get_type_by_address(address_01)
    type_02 = get_type_by_address(address_02)
    if type_01 != type_02:
        raise Exception("Type mismatch exception.")


def assignment(self, _tree: Tree):
    """Creates the assignment quadruple.

    Creates an assignment quadruple where the first expression variable will
    be set to the second expression variable.

    Raises an error if the expression types are incompatible.

    `assignment: var_exp ASSIGNMENT (read | expression) _LINE_END`
    """
    assignor: int = self.addresses_stack.pop()
    asignee: int = self.addresses_stack.pop()
    if in_data_segment(assignor) and in_data_segment(asignee):
        check_operations(assignor, asignee)
    quad = (AssignmentOperators.ASSIGN, asignee, assignor)
    self.quadruples.append(quad)
