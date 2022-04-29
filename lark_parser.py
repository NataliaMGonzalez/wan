from lark import Lark


def parseTree(grammar, code):
    return Lark(grammar).parse(code)
