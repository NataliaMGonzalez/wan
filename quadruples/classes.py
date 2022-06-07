from addresses_manager import assign_into_extra_segment, assign_temporal
import globals
from typing import Union
from lark import Token, Tree
from enums import ClassOperations, DataTypes


primitive_types = set(type.value for type in DataTypes)


def get_instance_attribute(self, tree: Union[Token, Tree]) -> int:
    """Create the quadruples for getting the value from an instance.

    When reading an instance variable, get the address from its variables table
    or from the function inside of the class.
    `instance_attribute: var_exp _INSTANCE_ATTRIBUTE (VAR_ID | function_eval)`
    """
    _, var_or_function = tree.children

    vars_table = self.variables_table

    # Due to the first section of the rule being var_exp, because it was a
    # class, this will now be on the top of the addresses_stack
    class_address = self.addresses_stack.pop()
    class_type = vars_table[(class_address, "type")]

    # In case the second parameter is a function, return that function's address.
    is_function: bool = isinstance(var_or_function, Tree)
    if is_function:
        function_name = var_or_function.children[1].children[0].value
        return globals.functions_directory[class_type][function_name][
            "returns"]

    # Get the class type and assign the pointer based on it
    var_name = var_or_function.value
    var_type = globals.class_prototypes[class_type][var_name]["type"]
    pointer_address = None
    if var_type in primitive_types:
        pointer_address = assign_temporal(DataTypes(var_type))
    else:
        pointer_address = assign_into_extra_segment()
        globals.variables_table[(pointer_address, "type")] = var_type

    quadruple = (ClassOperations.INSTANCE_ATTRIBUTE,
                 class_address, var_name, pointer_address)
    self.quadruples.append(quadruple)
    return pointer_address


def get_self_attribute(self, self_attribute: Tree) -> Union[ClassOperations, str]:
    """Create the quadruples to read from the class the execution is in.

    When reading an attribute from within a class, get it's variables table
    and place the corresponding quadruple. The context of which instance we are
    inside from is unknown.

    `self_attribute: _SELF_ATTRIBUTE _INSTANCE_ATTRIBUTE (VAR_ID | self_function)`
    """
    var_or_function = self_attribute.children[0]
    class_type = self.class_context

    # In case the parameter is a function, return that function's address.
    is_function: bool = isinstance(var_or_function, Tree)
    if is_function:
        function_name = var_or_function.children[1].children[0].value
        return globals.functions_directory[class_type][function_name][
            "returns"]

    # Get the class type and assign the pointer based on it
    var_name = var_or_function.value
    var_type = globals.class_prototypes[class_type][var_name]["type"]
    pointer_address = None
    if var_type in primitive_types:
        pointer_address = assign_temporal(DataTypes(var_type))
    else:
        pointer_address = assign_into_extra_segment()
        globals.variables_table[(pointer_address, "type")] = var_type

    quadruple = (ClassOperations.SELF_ATTRIBUTE, var_name, pointer_address)
    self.quadruples.append(quadruple)
    return pointer_address


def np_set_self_function(self, _tree: Tree):
    """Set the quadruples for setting the instance context for self function.

    When going into a self function `my:function()`, create a quadruple to
    set the current class context into the class we are inside in.
    """
    if self.class_context == None:
        raise Exception("Cannot call self attribute in global scope.")
    quadruple = (ClassOperations.SET_FUNCTION_CLASS,
                 ClassOperations.SELF_ATTRIBUTE)
    class_type = self.class_context
    self.classes_stack.append(class_type)
    self.quadruples.append(quadruple)


def np_clear_self_function(self, _tree: Tree):
    """Set the quadruples for clearing the instance context for self function.

    When exiting out of a self function `my:function()`, create a quadruple to
    clear the current class context for the function to be executed in.
    """
    quadruple = (ClassOperations.CLEAR_FUNCTION_CLASS,)
    self.quadruples.append(quadruple)


def np_set_class_function(self, _tree: Tree):
    """Set the quadruples for setting the instance context for instance function.

    When going into an instance function `instance:function()`, create a
    quadruple to set the current class context into the previously checked class.
    """
    class_address = self.addresses_stack[-1]
    quadruple = (ClassOperations.SET_FUNCTION_CLASS, class_address)
    vars_table = self.current_variables_table
    class_type = vars_table[(class_address, "type")]
    self.classes_stack.append(class_type)
    self.quadruples.append(quadruple)


def np_clear_class_function(self, _tree: Tree):
    """Set the quadruples for clearing the instance context for instance function.

    When exiting out of an instance function `instance:function()`, create a
    quadruple to clear the current class context for the function to be executed in.
    """
    quadruple = (ClassOperations.CLEAR_FUNCTION_CLASS,)
    self.quadruples.append(quadruple)
