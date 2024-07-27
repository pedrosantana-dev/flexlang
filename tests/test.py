import sys
import os

# Adiciona o diretório superior ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flexlang.lexer import lex, tokens
from flexlang.parser import Parser
from flexlang.interpreter import Interpreter

# Exemplo de uso
token_exprs = [(pattern, tag) for tag, pattern in tokens]

code = """
let x = 10;
let str = "Hello World!";
func add(a: Int, b: Int) -> Int {
    return a + b;
}
"""

def test_lexer():
    tokens = lex(code, token_exprs)
    for i, token in enumerate(tokens):
        print(f'{i} - {token}')
    print(f'Qtd. Tokens: {len(tokens)}')
    return tokens

def test_parser():
    tokens = test_lexer()
    parser = Parser(tokens)
    ast = parser.parse()
    print(f'AST: {ast}')
    return ast

def test_interpreter():
    ast = test_parser()
    interpreter = Interpreter()
    interpreter.interpret(ast)



# Exemplo de uma calculadora em FlexLang
def test_calculator():
    code = """
    func main() -> void {
        let a = input("Digite o primeiro número: ");
        let b = input("Digite o segundo número: ");
        
        let sum = add(a, b);
        let diff = subtract(a, b);
        let prod = multiply(a, b);
        let quot = divide(a, b);
        
        print("Sum: ", sum);
        print("Difference: ", diff);
        print("Product: ", prod);
        print("Quotient: ", quot);
    }

    func add(x: number, y: number) -> number {
        print("x: ", x, " y: ", y);
        return x + y;
    }

    func subtract(x: number, y: number) -> number {
        return x - y;
    }

    func multiply(x: number, y: number) -> number {
        return x * y;
    }

    func divide(x: number, y: number) -> number {
        return x / y;
    }

    main();
    """

    tokens = lex(code, token_exprs)
    # for i, token in enumerate(tokens):
    #     print(f'{i} - {token}')
    # print(f'Qtd. Tokens: {len(tokens)}')
    parser = Parser(tokens)
    ast = parser.parse()
    print(f'AST: {ast}')
    interpreter = Interpreter()
    interpreter.interpret(ast)

# test_interpreter()
test_calculator()