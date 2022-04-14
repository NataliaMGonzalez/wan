// Tokens
PROGRAM: "program"
START_CONDITIONAL: "if"
ALT_CONDITIONAL: "else"
WRITE_OPERATION: "print"
READ_OPERATION: "input"
CYCLE_START: "while"

FUNCTION_DECLARE: "action"
CLASS_DECLARE: "class"
COMMENT: /#[^\n]*/
FUNCTION_RETURN: "return"

REL_OP_LT: /</
REL_OP_GT: />/
REL_OP_NE: /<>/
REL_OP_EQ: /==/

BOOL_OP_AND: /&&/
BOOL_OP_OR: "||"
BOOL_OP_NE: /<>/

TYPE_BOOL: "bool"
TYPE_INT: "int"
TYPE_FLOAT: "float"
TYPE_CHAR: "char"
TYPE_STRING: "string"

BOOL_VALUE_TRUE: "true"
BOOL_VALUE_FALSE: "false"

INT_VALUE: /\d+/
FLOAT_VALUE: /\d+(\.\d+)?/
CHAR_VALUE: /'[^"]*'/
STRING_VALUE: /"[^"]*"/

CLASS_ID: /([A-Z][a-z0-9]+)+/
FUNCTION_ID: /\b[a-z][A-Za-z0-9]*\b/
VAR_ID: /\b[a-z_]+\b/

INHERITANCE: /<</
INSTANCE_ATTRIBUTE: /:/
SELF_ATTRIBUTE: "my"
OPEN_BLOCK: /{/
CLOSE_BLOCK: /}/
OPEN_GROUP: /\(/
CLOSE_GROUP: /\)/
ARRAY_START: /\[/
ARRAY_END: /\]/
LINE_END: ";"
MULTIPLE: /\,/

ASSIGNMENT: /=/
ARIT_OPS_SUM: /\+/
ARIT_OPS_SUBTRACT: /-/
ARIT_OPS_MULTIPLY: /\*/
ARIT_OPS_DIVIDE: /\//

NEGATIVE_NUMBER: /-/

NEW_LINE: /\n+/
WHITESPACE: (" " | /\t/ )+
%ignore WHITESPACE
%ignore NEW_LINE

// Rules
start: program

program: PROGRAM VAR_ID LINE_END global_statement_multiple

global_statement_multiple: global_statement global_statement_multiple |

global_statement: declaration | assignment | input_output  | function_call | comment

declaration: vars_declaration | function_declaration | class_declaration

declaration_type: TYPE_INT | TYPE_FLOAT | TYPE_CHAR | TYPE_BOOL | CLASS_ID

var_exp_array: ARRAY_START INT_VALUE ARRAY_END var_exp_array |

vars_declaration: declaration_type declaration_type_aux LINE_END

declaration_type_aux: VAR_ID var_exp_array  declaration_type_aux_2 |

declaration_type_aux_2: MULTIPLE declaration_type_aux |

function_declaration: FUNCTION_DECLARE function_declaration_aux | declaration_type function_declaration_aux

function_declaration_aux: FUNCTION_ID OPEN_GROUP function_parameters CLOSE_GROUP OPEN_BLOCK function_body CLOSE_BLOCK

function_parameters: declaration_type VAR_ID function_parameters_aux |

function_parameters_aux: MULTIPLE function_parameters |

function_body: function_statement_multiple | function_statement_multiple FUNCTION_RETURN expression

function_statement_multiple: function_statement function_statement_multiple | 

function_statement: vars_declaration | assignment | function_call | cycle | conditional | input_output | comment | FUNCTION_RETURN expression LINE_END

class_declaration: CLASS_DECLARE CLASS_ID class_inheritance OPEN_BLOCK class_body CLOSE_BLOCK

class_inheritance: INHERITANCE CLASS_ID |

class_body: vars_declaration class_body_aux| function_declaration class_body_aux | comment class_body_aux

class_body_aux: class_body |

assignment: VAR_ID assignment_aux | instance_attribute assignment_aux | self_attribute assignment_aux

assignment_aux: ASSIGNMENT expression LINE_END

expression: bool_exp | numerical_exp | char_exp | string_exp | var_exp | OPEN_GROUP expression CLOSE_GROUP

bool_exp: bool_constant | bool_operations | comparison | var_exp | OPEN_GROUP bool_exp CLOSE_GROUP

bool_constant: BOOL_VALUE_TRUE | BOOL_VALUE_FALSE

comparison: numerical_exp relop numerical_exp

relop: REL_OP_LT | REL_OP_GT | REL_OP_NE | REL_OP_EQ

bool_operations: bool_exp bool_op bool_exp

bool_op: BOOL_OP_AND | BOOL_OP_OR | REL_OP_NE

numerical_exp: numerical_constant | sum | var_exp | OPEN_GROUP numerical_exp CLOSE_GROUP

numerical_constant: negative_num INT_VALUE | negative_num FLOAT_VALUE

negative_num: NEGATIVE_NUMBER |

sum: term ARIT_OPS_SUM term | term ARIT_OPS_SUBTRACT term | term

term: factor ARIT_OPS_MULTIPLY factor | factor ARIT_OPS_DIVIDE factor | factor

factor: numerical_exp

char_exp: CHAR_VALUE | var_exp

string_exp: STRING_VALUE | var_exp

var_exp: VAR_ID | instance_attribute | self_attribute | function_eval | OPEN_GROUP var_exp CLOSE_GROUP | var_exp var_exp_array

instance_attribute: var_exp INSTANCE_ATTRIBUTE VAR_ID | var_exp INSTANCE_ATTRIBUTE function_eval

self_attribute: SELF_ATTRIBUTE INSTANCE_ATTRIBUTE VAR_ID

function_call: function_eval LINE_END | var_exp LINE_END

function_eval: FUNCTION_ID OPEN_GROUP arguments CLOSE_GROUP

arguments: expression | expression MULTIPLE arguments | 

conditional: START_CONDITIONAL OPEN_GROUP bool_exp CLOSE_GROUP OPEN_BLOCK function_statement_multiple CLOSE_BLOCK conditional_aux

conditional_aux: ALT_CONDITIONAL OPEN_BLOCK function_statement_multiple CLOSE_BLOCK |

cycle: CYCLE_START OPEN_GROUP bool_exp CLOSE_GROUP OPEN_BLOCK function_statement_multiple CLOSE_BLOCK

input_output: read | write 

read: READ_OPERATION OPEN_GROUP filename CLOSE_GROUP LINE_END

filename: STRING_VALUE

write: WRITE_OPERATION OPEN_GROUP expression CLOSE_GROUP LINE_END

comment: COMMENT