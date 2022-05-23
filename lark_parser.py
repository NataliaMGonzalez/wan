from lark import Lark


def parseTree(grammar, code):
    return Lark(grammar, propagate_positions=True).parse(code)
