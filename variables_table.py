from lark import Visitor
from enums import DataTypes
from numpy import prod
from memory_manager import assign_to_memory


def generate_variables_table(tree):
    VariablesTable().visit_topdown(tree)
    return VariablesTable.variables_table


def get_table(variables_table, class_context=None, function_context=None):
    if class_context is not None and function_context is not None:
        return variables_table[class_context][function_context]
    elif function_context is not None:
        return variables_table[function_context]
    elif class_context is not None:
        return variables_table[class_context]
    return variables_table


def get_declarations(vars_declaration_id):
    declarations = []
    while (vars_declaration_id is not None):
        var_name, *array_sizes, next_var = vars_declaration_id.children
        sizes = list(map(lambda s: int(s.value), array_sizes))
        declarations.append((var_name.value, sizes))
        vars_declaration_id = next_var
    return declarations


class VariablesTable(Visitor):
    class_context = None
    function_context = None
    variables_table = {}

    def class_declaration(self, tree):
        class_id = tree.children[1].value
        self.class_context = class_id
        self.variables_table[class_id] = {}

    def np_end_class_declaration(self, _tree):
        self.class_context = None

    def function_declaration(self, tree):
        function_id = tree.children[1].value
        self.function_context = function_id
        table = get_table(self.variables_table, self.class_context)
        table[function_id] = {}

    def np_end_function_declaration(self, _tree):
        self.function_context = None

    def vars_declaration(self, tree):
        declaration_type, vars_declaration_id, _ = tree.children
        var_type = DataTypes[declaration_type.children[0].value.upper()]
        table = get_table(self.variables_table,
                          self.class_context, self.function_context)
        declarations = get_declarations(vars_declaration_id)
        for var_name, array_sizes in declarations:
            new_address = assign_to_memory(var_type, None)
            table[var_name] = new_address
            total_size = int(prod(array_sizes))
            if len(array_sizes) > 0:
                table[(var_name, "size")] = array_sizes
            for _ in range(1, total_size):
                assign_to_memory(var_type, None)

    def np_end_vars_declaration(self, _tree):
        self.function_context = None
