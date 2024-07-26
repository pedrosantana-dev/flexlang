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
        elif isinstance(node, FuncCall):
            func = self.environment[node.name]
            args = [self.interpret(arg) for arg in node.args]
            local_env = {param.name: arg for param, arg in zip(func.params, args)}
            return self._execute_function(func, local_env)
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
        elif isinstance(node, Num):
            return int(node.value)
        elif isinstance(node, Indentifier):
            return self.environment[node.name]
        elif isinstance(node, If):
            condition = self.interpret(node.condition)
            if condition:
                return self.interpret(node.then_branch)
            elif node.else_branch:
                return self.interpret(node.else_branch)
        elif isinstance(node, For):
            start = self.interpret(node.start)
            end = self.interpret(node.end)
            for i in range(start, end):
                self.environment[node.var] = i
                self.interpret(node.body)

    def _execute_function(self, func, local_env):
        old_env = self.environment
        self.environment = local_env
        try:
            for statement in func.body:
                self.interpret(statement)
        finally:
            self.environment = old_env