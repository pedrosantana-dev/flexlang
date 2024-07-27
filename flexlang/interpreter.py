from flexlang.ast import *


class Interpreter:
    def __init__(self):
        self.environment = {}

    def interpret(self, node):
        if isinstance(node, Program):
            for statement in node.statements:
                self.interpret(statement)
        elif isinstance(node, VarDecl):
            value = self.evaluate(node.value)
            print(f'VarDecl: {node.name} = {value}')
            self.environment[node.name] = value
        elif isinstance(node, FuncDecl):
            self.environment[node.name] = node
        elif isinstance(node, ReturnStmt):
            return self.evaluate(node.value)
        elif isinstance(node, ExprStmt):
            return self.evaluate(node.expr)
        elif isinstance(node, Identifier):
            return self.evaluate(node)
        
    def execute(self, stmt):
        if isinstance(stmt, VarDecl):
            value = self.evaluate(stmt.value)
            print(f'VarDecl: {stmt.name} = {value}')
            self.environment[stmt.name] = value
        elif isinstance(stmt, FuncDecl):
            self.environment[stmt.name] = stmt
        elif isinstance(stmt, ReturnStmt):
            return self.evaluate(stmt.value)
        elif isinstance(stmt, ExprStmt):
            return self.evaluate(stmt.expr)

    def evaluate(self, expr):
        if isinstance(expr, Num):
            return expr.value
        elif isinstance(expr, String):
            return expr.value
        elif isinstance(expr, Identifier):
            return self.environment.get(expr.name)
        elif isinstance(expr, BinOp):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)
            if expr.op.type == 'PLUS':
                return left + right
            elif expr.op.type == 'MINUS':
                return left - right
            elif expr.op.type == 'TIMES':
                return left * right
            elif expr.op.type == 'DIVIDE':
                return left / right
        elif isinstance(expr, UnaryOp):
            right = self.evaluate(expr.right)
            if expr.op.type == 'MINUS':
                return -right
        elif isinstance(expr, Input):
            prompt = self.evaluate(expr.prompt)
            return float(input(prompt))
        elif isinstance(expr, Print):
            values = [self.evaluate(v) for v in expr.values]
            print(" ".join(map(str, values)))
        elif isinstance(expr, FuncCall):
            func = self.environment[expr.callee.name]
            if func is None:
                raise Exception(f'Undefined function {expr.callee.name}')
            args = [self.evaluate(arg) for arg in expr.args]
            local_env = self.environment.copy()
            for param, arg in zip(func.parameters, args):
                local_env[param.name.value] = arg
            old_environment = self.environment.copy()
            self.environment = local_env
            for stmt in func.body:
                result = self.execute(stmt)
                print(f'Soma interna: {result}')
                if isinstance(result, ReturnStmt):
                    return result.value
            self.environment = old_environment
            return None

        raise Exception(f'Unknown expression type {type(expr)}')
