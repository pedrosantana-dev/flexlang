from flexlang.ast import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        statements = []
        while not self._is_at_end():
            stmt = self._statement()
            if stmt is not None:
                statements.append(stmt)
        return Program(statements)
    
    def _statement(self):
        if self._match('LET'):
            return self._var_decl()
        elif self._match('FUNC'):
            return self._func_decl()
        elif self._match('RETURN'):
            return self._return_stmt()
        elif self._match('IF'):
            return self._if_stmt()
        elif self._match('FOR'):
            return self._for_stmt()
        else:
            self._expression_stmt()
    
    def _var_decl(self):
        token = self._consume('ID', 'Expected identifier')
        self._consume('ASSIGN', 'Expected "="')
        value = self._expression()
        self._consume('END', 'Expected ";"')
        return VarDecl(token.value, None, value)
    
    def _func_decl(self):
        token = self._consume('ID', 'Expected identifier')
        self._consume('LPAREN', 'Expected "("')
        params = self._parameters()
        self._consume('RPAREN', 'Expected ")"')
        self._consume('ARROW', 'Expected "->"')
        return_type = self._type()
        self._consume('LBRACE', 'Expected "{"')
        body = []
        while not self._check('RBRACE'):
            stmt = self._statement()
            if stmt is not None:
                body.append(stmt)
        self._consume('RBRACE', 'Expected "}"')
        return FuncDecl(token.value, params, return_type, body)
    
    def _return_stmt(self):
        value = None
        if not self._check('END'):
            value = self._expression()
        self._consume('END', 'Expected ";"')
        return ReturnStmt(value)
    
    def _if_stmt(self):
        self._consume('LPAREN', 'Expected "("')
        condition = self._expression()
        self._consume('RPAREN', 'Expected ")"')
        then_branch = self._statement()
        else_branch = None
        if self._match('ELSE'):
            else_branch = self._statement()
        return If(condition, then_branch, else_branch)
    
    def _for_stmt(self):
        self._consume('LPAREN', 'Expected "("')
        var = self._var_decl()
        self._consume('IN', 'Expected "in"')
        start = self._expression()
        self._consume('TO', 'Expected "to"')
        end = self._expression()
        self._consume('RPAREN', 'Expected ")"')
        body = self._statement()
        return For(var, start, end, body)
    
    def _parameters(self):
        params = []
        if not self._check('RPAREN'):
            params.append(self._parameter())
            while self._match('COMMA'):
                params.append(self._parameter())
        return params
    
    def _parameter(self):
        token = self._consume('ID', 'Expected parameter name')
        self._consume('COLON', 'Expected ":"')
        type = self._type()
        identifier = Identifier(token.value)
        return Param(identifier, type)
    
    def _type(self):
        return self._consume('ID', 'Expected type')
    
    def _expression(self):
        return self._assignment()
    
    def _assignment(self):
        expr = self._or()
        if self._match('ASSIGN'):
            value = self._expression()
            return Assign(expr, value)
        return expr
    
    def _or(self):
        expr = self._and()
        while self._match('OR'):
            op = self._previous()
            right = self._and()
            expr = BinOp(expr, op, right)
        return expr
    
    def _and(self):
        expr = self._equality()
        while self._match('AND'):
            op = self._previous()
            right = self._equality()
            expr = BinOp(expr, op, right)
        return expr
    
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
        return self._call()
    
    def _call(self):
        expr = self._primary()
        while True:
            if self._match('LPAREN'):
                expr = self._finish_call(expr)
            else:
                break
        return expr
    
    def _finish_call(self, callee):
        args = []
        if not self._check('RPAREN'):
            args.append(self._expression())
            while self._match('COMMA'):
                args.append(self._expression())
        self._consume('RPAREN', 'Expected ")"')
        return FuncCall(callee, args)
    
    def _primary(self):
        if self._match('NUMBER'):
            return Num(self._previous().value)
        elif self._match('STRING'):
            return String(self._previous().value)
        elif self._match('ID'):
            return Identifier(self._previous().value)
        elif self._match('LPAREN'):
            expr = self._expression()
            self._consume('RPAREN', 'Expected ")"')
            return expr
        elif self._match('INPUT'):
            self._consume('LPAREN', 'Expected "("')
            prompt = self._expression()
            self._consume('RPAREN', 'Expected ")"')
            return Input(prompt)
        elif self._match('PRINT'):
            self._consume('LPAREN', 'Expected "("')
            values = [self._expression()]
            while self._match('COMMA'):
                values.append(self._expression())
            self._consume('RPAREN', 'Expected ")"')
            return Print(values)
        else:
            raise RuntimeError('Expected expression')
    
    def _expression_stmt(self):
        expr = self._expression()
        self._consume('END', 'Expected ";"')
        return ExprStmt(expr)
    
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