from typing import List
from addresses_manager import assign_instance_to_memory, assign_primitive_to_memory
from collections import OrderedDict
from lark import Tree
from lark.visitors import Visitor_Recursive
from enums import DataTypes
from numpy import prod
from variables_table.classes_variables import generate_classes_variables


primitive_types = set(type.value for type in DataTypes)


def generate_variables_table(tree: Tree):
    classes_variables = generate_classes_variables(tree)
    vars_table_object = VariablesTable()
    vars_table_object.classes_variables = classes_variables
    vars_table_object.visit(tree)
    return VariablesTable.variables_table


class VariablesTable(Visitor_Recursive):
    class_context = None
    function_context = None
    variables_table = OrderedDict()
    classes_variables = OrderedDict()

    # Class instances that have not been properly declared yet
    remaining_instances = []

    @property
    def current_table(self) -> OrderedDict:
        table = self.variables_table
        if self.class_context is not None:
            table = table[self.class_context]
        if self.function_context is not None:
            table = table[self.function_context]
        return table

    def class_id(self, tree):
        class_id = tree.children[0].value
        self.classes_variables[class_id] = OrderedDict()
        self.current_table[class_id] = OrderedDict()
        self.class_context = class_id

    def class_inheritance(self, tree: Tree):
        class_id = self.class_context
        parent_id = tree.children[0].value
        parent_table = self.classes_variables[parent_id]
        for key in parent_table:
            self.classes_variables[class_id][key] = parent_table[key]

    def class_declaration(self, _tree):
        self.class_context = None

    def function_id(self, tree):
        function_id = tree.children[0].value
        self.current_table[function_id] = OrderedDict()
        self.function_context = function_id

    def function_parameter(self, tree):
        var_type, var_name = tree.children
        var_type = DataTypes(var_type.value)
        new_address = assign_primitive_to_memory(var_type)
        table = self.current_table
        table[var_name.value] = new_address

    def function_declaration(self, _tree):
        self.function_context = None

    def vars_declaration(self, tree: Tree):
        declaration_type, *declaration_ids = tree.children
        var_type: str = declaration_type.value
        # In case we are inside class, do not declare. These will be handled when the class is instantiated.
        if self.class_context is not None:
            return
        current_table = self.current_table
        for declaration in declaration_ids:
            var_name, *array_sizes = declaration.children
            var_name = var_name.value
            sizes = list(map(lambda s: int(s.value), array_sizes))
            add_variable_to_table(self, current_table,
                                  var_type, var_name, sizes)


def add_variable_to_table(
        self, vars_table: OrderedDict, var_type: str, var_name: str,
        sizes: List[int]):
    if var_name in vars_table:
        error_message = "Variable \"{}\" already declared in this scope.".format(
            var_name)
        raise TypeError(error_message)
    new_address = save_variable_in_memory(self, var_type, var_name)
    vars_table[var_name] = new_address
    total_size = int(prod(sizes))
    if len(sizes) > 0:
        vars_table[(new_address, "size")] = sizes
    for _ in range(1, total_size):
        save_variable_in_memory(self, var_type)


def save_variable_in_memory(self, var_type: str, var_name: str = None):
    is_primitive = var_type in primitive_types
    if is_primitive:
        return assign_primitive_to_memory(DataTypes(var_type))
    else:
        if var_name is not None:
            self.variables_table[var_name] = None
        new_address = instantiate_class(self, var_type)
        if var_name is not None:
            self.variables_table[var_name] = new_address
        return new_address


def instantiate_class(self, class_type: str) -> int:
    new_address = assign_instance_to_memory()
    self.variables_table[new_address] = OrderedDict()
    self.variables_table[(new_address, "type")] = class_type
    instance_table = self.variables_table[new_address]
    class_variables = self.classes_variables[class_type]
    for variable in class_variables:
        var_type = class_variables[variable]["type"]
        var_name = class_variables[variable]["name"]
        sizes = class_variables[variable]["sizes"]
        add_variable_to_table(self, instance_table, var_type, var_name, sizes)
    return new_address
