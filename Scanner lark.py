from lark import Lark

parser = Lark(open("lark_tokens_rules.g", 'r').read())
calc = parser.parse
s = open("ejemplo.wan", 'r').read()
print(calc(s).pretty())