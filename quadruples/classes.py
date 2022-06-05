from addresses_manager import assign_into_extra_segment
import globals
from typing import Union
from lark import Token, Tree
from enums import ClassOperations


def get_instance_attribute(self, tree: Union[Token, Tree]) -> int:
    """
    When reading a class instance, get the address from its variables table.
    `instance_attribute: var_exp _INSTANCE_ATTRIBUTE (VAR_ID | function_eval)`
    """
    _, var_or_function = tree.children

    # Due to the first section of the rule being var_exp, because it was a
    # class, this will now be on the top of the addresses_stack
    class_address = self.addresses_stack.pop()

    vars_table = self.variables_table

    # In case the second parameter is a function, return that function's address.
    is_function: bool = isinstance(var_or_function, Tree)
    if is_function:
        function_name = var_or_function.children[1].children[0].value
        class_type = vars_table[(class_address, "type")]
        return globals.functions_directory[class_type][function_name][
            "returns"]

    var_name = var_or_function.value
    pointer_address = assign_into_extra_segment()
    quadruple = (ClassOperations.INSTANCE_ATTRIBUTE,
                 class_address, var_name, pointer_address)
    self.quadruples.append(quadruple)
    return pointer_address


def get_self_attribute(self, self_attribute: Tree) -> Union[ClassOperations, str]:
    var_or_function = self_attribute.children[0]

    # In case the parameter is a function, return that function's address.
    is_function: bool = isinstance(var_or_function, Tree)
    if is_function:
        function_name = var_or_function.children[1].children[0].value
        class_type = self.class_context
        return globals.functions_directory[class_type][function_name][
            "returns"]

    var_name = var_or_function.value
    pointer_address = assign_into_extra_segment()
    quadruple = (ClassOperations.SELF_ATTRIBUTE, var_name, pointer_address)
    self.quadruples.append(quadruple)
    return pointer_address


def np_set_self_function(self, _tree: Tree):
    if self.class_context == None:
        raise Exception("Cannot call self attribute in global scope.")
    quadruple = (ClassOperations.SET_FUNCTION_CLASS,
                 ClassOperations.SELF_ATTRIBUTE)
    class_type = self.class_context
    self.classes_stack.append(class_type)
    self.quadruples.append(quadruple)


def np_clear_self_function(self, _tree: Tree):
    quadruple = (ClassOperations.CLEAR_FUNCTION_CLASS,)
    self.quadruples.append(quadruple)


def np_set_class_function(self, _tree: Tree):
    class_address = self.addresses_stack[-1]
    quadruple = (ClassOperations.SET_FUNCTION_CLASS, class_address)
    vars_table = self.current_variables_table
    class_type = vars_table[(class_address, "type")]
    self.classes_stack.append(class_type)
    self.quadruples.append(quadruple)


def np_clear_class_function(self, _tree: Tree):
    quadruple = (ClassOperations.CLEAR_FUNCTION_CLASS,)
    self.quadruples.append(quadruple)
