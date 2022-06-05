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
    """
    Traverse the code to generate the variables table to be used for the
    functions directory creation and the quadruples creation.
    """
    classes_variables = generate_classes_variables(tree)
    vars_table_object = VariablesTable()
    vars_table_object.classes_variables = classes_variables
    vars_table_object.visit(tree)
    return VariablesTable.variables_table


class VariablesTable(Visitor_Recursive):
    """Traverses all the neuralgic points placed accross the grammar in order to
    generate the variables table.
    """

    variables_table = OrderedDict()    # The final variables table

    class_context = None               # If we are inside a class
    function_context = None            # If we are inside a function

    # Variables each class contains, to be used when instantiating the classes
    classes_variables = OrderedDict()

    @property
    def current_table(self) -> OrderedDict:
        """The table of the actual context and only the actual context."""
        table = self.variables_table
        if self.class_context is not None:
            table = table[self.class_context]
        if self.function_context is not None:
            table = table[self.function_context]
        return table

    def class_id(self, tree: Tree):
        """Set the class context to indicate we are now inside a class.
        `class_id: CLASS_ID`
        """
        class_id: str = tree.children[0].value
        self.current_table[class_id] = OrderedDict()
        self.class_context = class_id

    def class_declaration(self, _tree: Tree):
        """Once we finish traversing the class, indicate that we are now outside.
        `class_id: CLASS_ID`
        """
        self.class_context = None

    def function_id(self, tree: Tree):
        """Set the function context to indicate we are now inside a function.
        \n`function_id: FUNCTION_ID`
        """
        function_id: str = tree.children[0].value
        self.current_table[function_id] = OrderedDict()
        self.function_context = function_id

    def function_declaration(self, _tree: Tree):
        """Once we finish traversing the function, indicate that we are now outside.
        `function_declaration: (FUNCTION_DECLARE | declaration_type) function_id _OPEN_GROUP _function_parameters _CLOSE_GROUP _OPEN_BLOCK function_body _CLOSE_BLOCK`
        """
        self.function_context = None

    def function_parameter(self, tree: Tree):
        """Assign parameter in variables table and add it to the function's table.
        `function_parameter: declaration_type VAR_ID`
        """
        var_type, var_name = tree.children
        var_type = DataTypes(var_type.value)
        new_address = assign_primitive_to_memory(var_type)
        table = self.current_table
        table[var_name.value] = new_address

    def vars_declaration(self, tree: Tree):
        """Add the variables declared into the variables table in the current context.
        `vars_declaration: declaration_type vars_declaration_id (_MULTIPLE vars_declaration_id)* _LINE_END`
        """
        # In case we are inside class, do not declare. These will be handled when the class is instantiated.
        if self.class_context is not None:
            return
        declaration_type, *declaration_ids = tree.children
        var_type: str = declaration_type.value
        current_table = self.current_table
        for declaration in declaration_ids:
            var_name, *array_sizes = declaration.children
            var_name: str = var_name.value
            sizes = list(map(lambda s: int(s.value), array_sizes))
            add_variable_to_table(self, current_table,
                                  var_type, var_name, sizes)


def add_variable_to_table(
        self, vars_table: OrderedDict, var_type: str, var_name: str,
        sizes: List[int]):
    """Allocate a space in memory and add the resulting address into the variables table."""
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
    """Depending on the variable type, takes a space in memory to place the variable."""
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
    """Goes through the classes variables to take a space in memory for each of their parameters."""
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
