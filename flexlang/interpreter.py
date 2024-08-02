from flexlang.ast import *


class Interpreter:
    def __init__(self):
        self.environment = {}

    def interpret(self, program):
        if isinstance(program, Program):
            print(f'Program statements: {program.statements}')
            for statement in program.statements:
                self._evaluate(statement)
        else:
            raise Exception(f'Unknown program type {type(program)}')                

    def _evaluate(self, node):
        print(f'Evaluate: {node}')
        if isinstance(node, Num):
            return node.value
        elif isinstance(node, String):
            return node.value
        elif isinstance(node, VarDecl):
            self.environment[node.name] = self._evaluate(node.value)
            return None
        elif isinstance(node, Identifier):
            print(f'Identifier: {node.name}')
            return self.environment.get(node.name)
        elif isinstance(node, BinOp):
            left = self._evaluate(node.left)
            right = self._evaluate(node.right)
            if node.op.type == 'PLUS':
                return left + right
            elif node.op.type == 'MINUS':
                return left - right
            elif node.op.type == 'TIMES':
                return left * right
            elif node.op.type == 'DIVIDE':
                return left / right
        elif isinstance(node, UnaryOp):
            right = self._evaluate(node.right)
            if node.op.type == 'MINUS':
                return -right
        elif isinstance(node, Input):
            prompt = self._evaluate(node.prompt)
            return float(input(prompt))
        elif isinstance(node, Print):
            print('Executar print')
            values = [self._evaluate(v) for v in node.values]
            print(" ".join(map(str, values)))
            return None
        elif isinstance(node, ExprStmt):
            return self._evaluate(node.expr)
        elif isinstance(node, ReturnStmt):
            return node.value
        elif isinstance(node, FuncDecl):
            self.environment[node.name] = node
            return None
        elif isinstance(node, FuncCall):
            print(f'FuncCall: {node.callee.name}')
            func = self.environment[node.callee.name]
            if func is None:
                raise Exception(f'Undefined function {node.callee.name}')
            args = [self._evaluate(arg) for arg in node.args]
            local_env = self.environment.copy()
            for param, arg in zip(func.parameters, args):
                local_env[param.identifier.name] = arg
            old_environment = self.environment.copy()
            self.environment = local_env
            for stmt in func.body:
                result = self._evaluate(stmt)
                if result is not None:
                    return self._evaluate(result)
            self.environment = old_environment
            return None

        raise Exception(f'Unknown expression type {type(node)}')
