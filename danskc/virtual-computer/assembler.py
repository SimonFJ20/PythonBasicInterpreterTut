from typing import List
from assembler.symbols import SymbolTable, find_symbols
from assembler.parser import Line, Operation, parse_lines

def check_operations(operations: List[Operation], symbols: SymbolTable) -> None:
    for operation in operations:
        if operation.operator == "noop":
            if len(operation.operands) != 0:
                raise Exception(f"\"{len(operation.operands)}\" instruction expects 0 arguments, {len(operation.operands)} was given")
        elif operation.operator == "jmp":
            if len(operation.operands) != 1:
                raise Exception(f"\"{len(operation.operands)}\" instruction expects 1 argument, {len(operation.operands)} was given")
        elif operation.operator == "jnz":
            if len(operation.operands) != 2:
                raise Exception(f"\"{len(operation.operands)}\" instruction expects 2 arguments, {len(operation.operands)} was given")
        elif operation.operator == "mov":
            if len(operation.operands) != 2:
                raise Exception(f"\"{len(operation.operands)}\" instruction expects 2 arguments, {len(operation.operands)} was given")
        elif operation.operator == "load":
            if len(operation.operands) != 2:
                raise Exception(f"\"{len(operation.operands)}\" instruction expects 2 arguments, {len(operation.operands)} was given")
        elif operation.operator == "store":
            if len(operation.operands) != 2:
                raise Exception(f"\"{len(operation.operands)}\" instruction expects 2 arguments, {len(operation.operands)} was given")
        elif operation.operator in ["and", "or", "xor", "add", "sub", "mul", "div", "mod", "shl", "cmp", "lt"]:
            if len(operation.operands) != 2:
                raise Exception(f"\"{len(operation.operands)}\" instruction expects 2 arguments, {len(operation.operands)} was given")
        else:
            raise Exception(f"unknown instruction \"{operation.operator}\"")



def assemble(text: str) -> str:
    lines = parse_lines(text)
    symbols = find_symbols(lines)
    # return "[\n" + ",".join([" ".join(line.to_json().split()) for line in lines]) + "\n]"
    lines = [line for line in lines if line.operation]

if __name__ == "__main__":
    from argparse import ArgumentParser
    argparser = ArgumentParser()
    argparser.add_argument("file")
    args = argparser.parse_args()
    with open(args.file) as file:
        # print(assemble(file.read()), end="", flush=True)
        print(assemble(file.read()))
    
