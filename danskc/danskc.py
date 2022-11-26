from __future__ import annotations
from checker import check_top_level_statements
from parser_ import Parser, parsed_statements_to_string
from tokenizer import tokenize


def main() -> None:
    with open("test.dk") as file:
        text = file.read()
        print("\nTOKENIZING...\n")
        tokens = tokenize(text)
        print("\n=== TOKEN ===\n")
        for token in tokens:
            print(token)
        print("\nPARSING...\n")
        parser = Parser(tokens)
        parsed_ast = parser.parse_statements()
        print("\n=== PARSEDAST ===\n")
        print(parsed_statements_to_string(parsed_ast))
        print("\nCHECKING...\n")
        checked_ast = check_top_level_statements(parsed_ast)
        print("\n=== CHECKED AST ===\n")


if __name__ == "__main__":
    main()
