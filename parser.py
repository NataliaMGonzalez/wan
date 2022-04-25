from lark import Lark

parser = Lark(open("grammar.lark", 'r').read())
calc = parser.parse
s = open("example.wan", 'r').read()
print(calc(s).pretty())