from __future__ import annotations
from parser import Parser, statements_to_string
from tokenizer import tokenize


def main() -> None:
    with open("test.dk") as file:
        text = file.read()
        tokens = tokenize(text)
        parser = Parser(tokens)
        print("=== TOKEN ===")
        for token in tokens:
            print(token)
        ast = parser.parse_statements()
        print("=== AST ===")
        print(statements_to_string(ast))


if __name__ == "__main__":
    main()
