import sys
import os

# Adiciona o diretório superior ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flexlang.lexer import lex, tokens

# Exemplo de uso
token_exprs = [(pattern, tag) for tag, pattern in tokens]

code = """
let x = 10;
func add(a: Int, b: Int) -> Int {
    return a + b;
}
"""

print(lex(code, token_exprs))