from flexlang.ast import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        statements = []
        while not self._is_at_end():
            statements.append(self._statement())
        return Program(statements)
    
    def _statement(self):
        if self._match('LET'):
            return self._var_decl()
        elif self._match('FUNC'):
            return self._func_decl()
        else:
            raise RuntimeError('Unexpected statement')
    
    def _var_decl(self):
        name = self._consume('ID', 'Expected indentifier')
        self._consume('ASSIGN', 'Expected "="')
        value = self._expression()
        self._consume('END', 'Expected ";"')
        return VarDecl(name, None, value)
    
    def _func_decl(self):
        name = self._consume('ID', 'Expected indentifier')
        self._consume('LPAREN', 'Expected "("')
        params = self._parameters()
        self._consume('RPAREN', 'Expected ")"')
        self._consume('ARROW', 'Expected "->"')
        return_type = self._type()
        self._consume('LBRACE', 'Expected "{"')
        body = []
        while not self._check('RBRACE'):
            body.append(self._statement())
        self._consume('RBRACE', 'Expected "}"')
        return FuncDecl(name, params, return_type, body)
    
    def _parameters(self):
        params = []
        if not self._check('RPAREN'):
            params.append(self._parameter())
            while self._match('COMMA'):
                params.append(self._parameter())
        return params
    
    def _parameter(self):
        name = self._consume('ID', 'Expected parameter name')
        self._consume('COLON', 'Expected ":"')
        type = self._type()
        return Param(name, type)
    
    def _type(self):
        return self._consume('ID', 'Expected type')
    
    def _expression(self):
        return self._equality()
    
    def _equality(self):
        expr = self._comparison()
        while self._match('EQUAL', 'BANG_EQUAL'):
            op = self._previous()
            right = self._comparison()
            expr = BinOp(expr, op, right)
        return expr
    
    def _comparison(self):
        expr = self._term()
        while self._match('GREATER', 'GREATER_EQUAL', 'LESS', 'LESS_EQUAL'):
            op = self._previous()
            right = self._term()
            expr = BinOp(expr, op, right)
        return expr
    
    def _term(self):
        expr = self._factor()
        while self._match('PLUS', 'MINUS'):
            op = self._previous()
            right = self._factor()
            expr = BinOp(expr, op, right)
        return expr
    
    def _factor(self):
        expr = self._unary()
        while self._match('TIMES', 'DIVIDE'):
            op = self._previous()
            right = self._unary()
            expr = BinOp(expr, op, right)
        return expr
    
    def _unary(self):
        if self._match('BANG', 'MINUS'):
            op = self._previous()
            right = self._unary()
            return UnaryOp(op, right)
        return self._primary()
    
    def _primary(self):
        if self._match('NUMBER'):
            return Num(self._previous().value)
        if self._match('ID'):
            return Indentifier(self._previous().value)
        if self._match('LPAREN'):
            expr = self._expression()
            self._consume('RPAREN', 'Expected ")"')
            return expr
        raise RuntimeError('Expected expression')
    
    def _match(self, *types):
        for type in types:
            if self._check(type):
                self._advance()
                return True
        return False
    
    def _consume(self, type, message):
        if self._check(type):
            return self._advance()
        raise RuntimeError(message)
    
    def _check(self, type):
        if self._is_at_end():
            return False
        return self._peek().type == type

    def _advance(self):
        if not self._is_at_end():
            self.pos += 1
        return self._previous()
    
    def _is_at_end(self):
        return self._peek().type == 'EOF'
    
    def _peek(self):
        return self.tokens[self.pos]
    
    def _previous(self):
        return self.tokens[self.pos - 1]