import re


# Definição dos tokens
tokens = [
    ('NUMBER',   r'\d+'),
    ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('ASSIGN',   r'='),
    ('END',      r';'),
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
    ('ARROW',    r'->'),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t]+'),
    ('MISMATCH', r'.')
]

# Palavras-chave
keywords = {'let', 'func', 'if', 'else', 'for', 'in', 'return', 'struct', 'goroutine'}


# Lexer
def lex(characters, token_exprs):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    if tag == 'ID' and text in keywords:
                        tag = text.upper()
                    token = (tag, text)
                    tokens.append(token)
                break
        if not match:
            raise RuntimeError(f'Unexpected character: {characters[pos]}')
        else:
            pos = match.end(0)
    return tokens