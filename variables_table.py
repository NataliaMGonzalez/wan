from addresses_manager import assign_to_memory, assign_into_extra_segment
from collections import OrderedDict
from lark import Tree
from lark.visitors import Visitor_Recursive
from enums import DataTypes
from numpy import prod


def generate_variables_table(tree):
    VariablesTable().visit(tree)
    return VariablesTable.variables_table


def add_class_variable(
        class_variables: OrderedDict, var_type: DataTypes, var_name: str,
        sizes: list):
    if var_name in class_variables:
        raise TypeError(
            "Variable \"{}\" already declared in this scope.".format(
                var_name))
    class_variables[var_name] = {
        "name": var_name,
        "type": var_type,
        "sizes": sizes,
    }


def add_variable_to_table(
        table: OrderedDict, var_type: DataTypes, var_name: str, sizes: list):
    if var_name in table:
        raise TypeError(
            "Variable \"{}\" already declared in this scope.".format(
                var_name))
    new_address = assign_to_memory(var_type)
    table[var_name] = new_address
    total_size = int(prod(sizes))
    if len(sizes) > 0:
        table[(var_name, "size")] = sizes
    for _ in range(1, total_size):
        assign_to_memory(var_type)


def instantiate_class(table, class_variables):
    for variable in class_variables:
        var_type = class_variables[variable]["type"]
        var_name = class_variables[variable]["name"]
        sizes = class_variables[variable]["sizes"]
        add_variable_to_table(table, var_type, var_name, sizes)


class VariablesTable(Visitor_Recursive):
    class_context = None
    function_context = None
    variables_table = OrderedDict()
    classes_variables = OrderedDict()

    def get_current_table(self):
        table = self.variables_table
        if self.class_context is not None:
            table = table[self.class_context]
        if self.function_context is not None:
            table = table[self.function_context]
        return table

    def class_id(self, tree):
        class_id = tree.children[0].value
        self.classes_variables[class_id] = OrderedDict()
        self.get_current_table()[class_id] = OrderedDict()
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
        self.get_current_table()[function_id] = OrderedDict()
        self.function_context = function_id

    def function_parameter(self, tree):
        var_type, var_name = tree.children
        var_type = DataTypes(var_type.value)
        new_address = assign_to_memory(var_type)
        table = self.get_current_table()
        table[var_name.value] = new_address

    def function_declaration(self, _tree):
        self.function_context = None

    def vars_declaration(self, tree: Tree):
        declaration_type, *declaration_ids = tree.children

        primitive_types = set(type.value for type in DataTypes)
        # Class instance
        if declaration_type not in primitive_types:
            class_type: str = declaration_type.value
            class_variables: OrderedDict = self.classes_variables[class_type]
            for declaration in declaration_ids:
                var_name, *array_sizes = declaration.children
                var_name = var_name.value
                sizes = list(map(lambda s: int(s.value), array_sizes))
                class_address = assign_into_extra_segment()
                self.get_current_table()[var_name] = class_address
                self.get_current_table()[class_address] = OrderedDict()
                self.get_current_table()[(class_address, "type")] = class_type
                instantiate_class(
                    self.get_current_table()[class_address],
                    class_variables)
                if len(sizes) > 0:
                    self.get_current_table()[(var_name, "size")] = sizes
                for _ in range(1, int(prod(sizes))):
                    class_address = assign_into_extra_segment()
                    self.get_current_table()[class_address] = OrderedDict()
                    class_table = self.get_current_table()[class_address]
                    instantiate_class(class_table, class_variables)
            return

        # Class variable
        var_type = DataTypes(declaration_type.value)
        if self.function_context is None and self.class_context is not None:
            class_variables = self.classes_variables[self.class_context]
            for declaration in declaration_ids:
                var_name, *array_sizes = declaration.children
                var_name = var_name.value
                sizes = list(map(lambda s: int(s.value), array_sizes))
                add_class_variable(class_variables, var_type, var_name, sizes)
                return

        # Regular declaration
        class_table = self.get_current_table()
        for declaration in declaration_ids:
            var_name, *array_sizes = declaration.children
            var_name = var_name.value
            sizes = list(map(lambda s: int(s.value), array_sizes))
            add_variable_to_table(class_table, var_type, var_name, sizes)
