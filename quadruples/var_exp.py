import globals
from collections import OrderedDict
from typing import Union
from lark import Token, Tree
from numpy import prod
from addresses_manager import assign_constant, assign_into_extra_segment
from enums import ArrayOperations, AssignmentOperators, ClassOperations, Operators


def var_exp(self, tree):
    variable = tree.children[0]
    var_address = get_variable_address(self, variable)
    self.addresses_stack.append(var_address)


def get_variable_address(self, variable: Union[Token, Tree]) -> int:
    """ Based on a variable token or tree, get the variable address. """
    if isinstance(variable, Token):
        variable_name: str = variable.value
        vars_table: OrderedDict = self.get_current_variables_table()
        if variable_name not in vars_table:
            raise Exception("Variable has not been previously declared.")
        return vars_table[variable_name]
    if (variable.data == "arr_exp"):
        return get_arr_exp(self, variable)
    if (variable.data == "self_attribute"):
        return get_self_attribute(self, variable)
    if (variable.data == "instance_attribute"):
        return get_instance_attribute(self, variable)
    if (variable.data == "function_eval"):
        return get_function_eval(self, variable)
    if (variable.data == "arr_exp_base"):
        return get_variable_address(self, variable.children[0])
    if (variable.data == "var_exp"):
        return get_variable_address(self, variable.children[0])


def get_function_eval(self, function_eval: Tree) -> int:
    """
    Address when the expression is a function evaluation.
    `function_eval: FUNCTION_ID _OPEN_GROUP expression? (_MULTIPLE expression)* _CLOSE_GROUP`
    """
    function_id = function_eval.children[0].value
    functions_directory = self.get_current_functions_directory()
    function_attributes = functions_directory[function_id]
    return_address = function_attributes["returns"]
    temp_address = assign_into_extra_segment()
    quad = (AssignmentOperators.ASSIGN, temp_address, return_address)
    self.quadruples.append(quad)
    return temp_address


def get_arr_exp(self, tree: Tree) -> int:
    """ Create quadruples to access exact address in array. """
    variable, *expressions = tree.children

    exp_addresses = []
    for _ in expressions:
        exp_address = self.addresses_stack.pop()
        exp_addresses = [exp_address] + exp_addresses
    base_address = get_variable_address(self, variable)

    vars_table = self.get_current_variables_table()
    size = vars_table[(base_address, "size")]

    # Calculate dimensions based on the array sizes
    dims = []
    for idx in range(len(size)):
        dims.append(int(prod(size[idx+1:])))

    total_sum_address = assign_into_extra_segment()
    zero = assign_constant(0)
    reset_quadruple = (AssignmentOperators.ASSIGN, total_sum_address, zero)
    self.quadruples.append(reset_quadruple)
    for exp_address, dim in zip(exp_addresses, dims):
        dim_address = assign_constant(dim)
        mult_address = assign_into_extra_segment()
        quad_multiply = (Operators.MULTIPLY, exp_address,
                         dim_address, mult_address)
        self.quadruples.append(quad_multiply)
        quad_sum = (Operators.ADD, mult_address,
                    total_sum_address, total_sum_address)
        self.quadruples.append(quad_sum)

    array_address = (base_address, total_sum_address)
    return array_address


def get_instance_attribute(self, tree: Union[Token, Tree]) -> int:
    """
    When reading a class instance, get the address from its variables table.
    `instance_attribute: var_exp _INSTANCE_ATTRIBUTE (VAR_ID | function_eval)`
    """
    _, var_or_function = tree.children

    # Due to the first section of the rule being var_exp, because it was a
    # class, this will now be on the top of the addresses_stack
    class_address = self.addresses_stack.pop()

    vars_table = self.get_current_variables_table()

    # In case the second parameter is a function, return that function's address.
    is_function: bool = isinstance(var_or_function, Tree)
    if is_function:
        function_name = var_or_function.children[1].children[0].value
        class_type = vars_table[(class_address, "type")]
        return globals.functions_directory[class_type][function_name][
            "returns"]

    var_name = var_or_function.value
    instance_table = vars_table[class_address]
    if var_name not in instance_table:
        raise Exception("This variable has not been defined.")

    return instance_table[var_name]


def get_self_attribute(self, self_attribute: Tree) -> Union[ClassOperations, str]:
    var_name = self_attribute.children[0].value
    return (ClassOperations.SELF_ATTRIBUTE, var_name)


def np_set_class_function(self, _tree: Tree):
    current_class = self.addresses_stack[-1]
    quadruple = (ClassOperations.SET_FUNCTION_CLASS, current_class)
    self.quadruples.append(quadruple)
    self.classes_stack.append(current_class)


def np_clear_class_function(self, _tree: Tree):
    quadruple = (ClassOperations.CLEAR_FUNCTION_CLASS,)
    self.quadruples.append(quadruple)
