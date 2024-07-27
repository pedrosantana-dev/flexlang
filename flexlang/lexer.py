import re


# Definição da Classe Token
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        return f'Token({self.type}, {self.value})'


# Definição dos tokens
tokens = [
    ('NUMBER',   r'\d+'),
    ('EQUAL',    r'=='),
    ('BANG_EQUAL', r'!='),
    ('GREATER_EQUAL', r'>='),
    ('LESS_EQUAL', r'<='),
    ('ARROW',    r'->'),
    ('PLUS',     r'\+'),
    ('MINUS',    r'-'),
    ('TIMES',    r'\*'),
    ('DIVIDE',   r'/'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('LBRACE',   r'\{'),
    ('RBRACE',   r'\}'),
    ('COMMA',    r','),
    ('COLON',    r':'),
    ('ASSIGN',   r'='),
    ('GREATER',  r'>'),
    ('LESS',     r'<'),
    ('BANG',     r'!'),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t]+'),
    ('PRINT',    r'\bprint\b'),
    ('LET',      r'\blet\b'),
    ('FUNC',     r'\bfunc\b'),
    ('RETURN',   r'\breturn\b'),
    ('IF',       r'\bif\b'),
    ('ELSE',     r'\belse\b'),
    ('FOR',      r'\bfor\b'),
    ('IN',       r'\bin\b'),
    ('STRUCT',   r'\bstruct\b'),
    ('GOROUTINE',r'\bgoroutine\b'),
    ('OR',       r'\bor\b'),
    ('AND',      r'\band\b'),
    ('END',      r';'),
    ('INPUT',    r'\binput\b'),
    ('STRING', r'"((?:\\.|[^"\\])*)"|\'((?:\\.|[\x20-\x7E])*)\''),
    ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
    # ('MISMATCH', r'.')
]

# Palavras-chave
keywords = {'let', 'func', 'if', 'else', 'for', 'in', 'return', 'struct', 'goroutine'}


# Lexer
def lex(characters, token_exprs):
    pos = 0
    tokens_list = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag == 'NEWLINE' or tag == 'SKIP':
                    pos = match.end(0)
                    break
                elif tag:
                    if tag == 'ID' and text in keywords:
                        tag = text.upper()
                    token = Token(tag, text)
                    tokens_list.append(token)
                pos = match.end(0)
                break
        if not match:
            raise RuntimeError(f'Unexpected character: {characters[pos]} at position {pos}')        
    tokens_list.append(Token('EOF', ''))
    return tokens_list