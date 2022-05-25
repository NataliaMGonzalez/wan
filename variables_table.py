from lark.visitors import Visitor_Recursive
from enums import DataTypes
from numpy import prod
from addresses_manager import assign_to_memory


def generate_variables_table(tree):
    VariablesTable().visit(tree)
    return VariablesTable.variables_table


class VariablesTable(Visitor_Recursive):
    class_context = None
    function_context = None
    variables_table = {}

    def get_current_table(self):
        table = self.variables_table
        if self.class_context is not None:
            table = table[self.class_context]
        if self.function_context is not None:
            table = table[self.function_context]
        return table

    def class_id(self, tree):
        class_id = tree.children[0].value
        self.get_current_table()[class_id] = {}
        self.class_context = class_id

    def class_declaration(self, _tree):
        self.class_context = None

    def function_id(self, tree):
        function_id = tree.children[0].value
        self.get_current_table()[function_id] = {}
        self.function_context = function_id

    def function_parameter(self, tree):
        var_type, var_name = tree.children
        var_type = DataTypes(var_type.value)
        new_address = assign_to_memory(var_type)
        table = self.get_current_table()
        table[var_name.value] = new_address

    def function_declaration(self, _tree):
        self.function_context = None

    def vars_declaration(self, tree):
        declaration_type, *declaration_ids = tree.children
        var_type = DataTypes(declaration_type.value)
        table = self.get_current_table()
        for declaration in declaration_ids:
            var_name, *array_sizes = declaration.children
            var_name = var_name.value
            if var_name in table:
                raise TypeError(
                    "Variable \"{}\" already declared in this scope.".format(
                        var_name))
            sizes = list(map(lambda s: int(s.value), array_sizes))
            new_address = assign_to_memory(var_type)
            table[var_name] = new_address
            total_size = int(prod(sizes))
            if len(sizes) > 0:
                table[(var_name, "size")] = sizes
            for _ in range(1, total_size):
                assign_to_memory(var_type)
