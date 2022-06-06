from collections import OrderedDict
from typing import Union
from lark import Token, Tree
from numpy import prod
from addresses_manager import assign_constant, assign_into_extra_segment, assign_temporal, get_type_by_address
from enums import ArrayOperations, AssignmentOperators, DataTypes, Operators
from quadruples.classes import get_instance_attribute, get_self_attribute


def var_exp(self, tree):
    variable = tree.children[0]
    var_address = get_variable_address(self, variable)
    self.addresses_stack.append(var_address)


def get_variable_address(self, variable: Union[Token, Tree]) -> int:
    """ Based on a variable token or tree, get the variable address. """
    if isinstance(variable, Token):
        variable_name: str = variable.value
        vars_table: OrderedDict = self.variables_table
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
    functions_directory = self.functions_directory
    function_attributes = functions_directory[function_id]
    return_address = function_attributes["returns"]
    return_type = get_type_by_address(return_address)
    temp_address = assign_temporal(return_type)
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

    vars_table = self.variables_table
    sizes = vars_table[(base_address, "size")]

    # Calculate dimensions based on the array sizes
    dims = []
    for idx in range(len(sizes)):
        dims.append(int(prod(sizes[idx+1:])))

    total_sum_address = assign_into_extra_segment()
    zero = assign_constant(0)
    reset_quadruple = (AssignmentOperators.ASSIGN, total_sum_address, zero)
    self.quadruples.append(reset_quadruple)
    for exp_address, size, dim in zip(exp_addresses, sizes, dims):
        dim_address = assign_constant(dim)
        verify_quad = (ArrayOperations.VERIFY, exp_address, size)
        self.quadruples.append(verify_quad)
        mult_address = assign_into_extra_segment()
        quad_multiply = (Operators.MULTIPLY, exp_address,
                         dim_address, mult_address)
        self.quadruples.append(quad_multiply)
        quad_sum = (Operators.ADD, mult_address,
                    total_sum_address, total_sum_address)
        self.quadruples.append(quad_sum)

    address_type = get_type_by_address(base_address)
    pointer_address = assign_temporal(address_type)
    quadruple = (ArrayOperations.POINT_TO, base_address,
                 total_sum_address, pointer_address)
    self.quadruples.append(quadruple)
    return pointer_address
