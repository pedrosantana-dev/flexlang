class ASTNode:
    pass


class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class VarDecl(ASTNode):
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value


class FuncDecl(ASTNode):
    def __init__(self, name, parameters, return_type, body):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.body = body


class FuncCall(ASTNode):
    def __init__(self, callee, args):
        self.callee: FuncDecl = callee
        self.args = args


class Param(ASTNode):
    def __init__(self, identifier, type):
        self.identifier: Identifier = identifier
        self.type = type


class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Num(ASTNode):
    def __init__(self, value):
        self.value = value

class String(ASTNode):
    def __init__(self, value):
        self.value = value


class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name


class UnaryOp(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr


class If(ASTNode):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class For(ASTNode):
    def __init__(self, var, start, end, body):
        self.var = var
        self.start = start
        self.end = end
        self.body = body

    
class ExprStmt(ASTNode):
    def __init__(self, expr):
        self.expr = expr


class ReturnStmt(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'ReturnStmt({self.value})'
    

class Input(ASTNode):
    def __init__(self, prompt):
        self.prompt = prompt


class Print(ASTNode):
    def __init__(self, values):
        self.values = values


class Assign(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value