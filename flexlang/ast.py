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


class Param(ASTNode):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Num(ASTNode):
    def __init__(self, value):
        self.value = value


class Indentifier(ASTNode):
    def __init__(self, name):
        self.name = name


class FuncCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args
