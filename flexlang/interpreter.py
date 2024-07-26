from flexlang.ast import *


class Interpreter:
    def __init__(self):
        self.environment = {}

    def interpret(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self.interpret(statement)
        elif isinstance(node, VarDecl):
            value = self.interpret(node.value)
            self.environment[node.name] = value
        elif isinstance(node, FuncDecl):
            self.environment[node.name] = node
        elif isinstance(node, BinOp):
            left = self.interpret(node.left)
            right = self.interpret(node.right)
            if node.op == '+':
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                return left / right