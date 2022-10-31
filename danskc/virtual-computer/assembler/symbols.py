from typing import Dict, List
from assembler.parser import Line

class SymbolTable:
    def __init__(self, global_symbols: Dict[str, int], local_symbols: Dict[str, List[int]]) -> None:
        self.global_symbols = global_symbols
        self.local_symbols = local_symbols
    

class SymbolTableBuilder:
    def __init__(self) -> None:
        self.global_symbols: Dict[str, int] = {}
        self.local_symbols: Dict[str, List[int]] = {}

    def build(self) -> SymbolTable:
        return SymbolTable(self.global_symbols, self.local_symbols)

    def define_local(self, name: str, lc: int) -> None:
        if name not in self.local_symbols:
            self.local_symbols[name] = []
        self.local_symbols[name].append(lc)

    def define_global(self, name, lc: int) -> None:
        if name in self.global_symbols:
            raise Exception(f"multiple defitions of symbol \"{name}\"")
        self.global_symbols[name] = lc

def instruction_size(operator: str) -> int:
    if operator == "noop":
        return 1
    elif operator in ["jmp", "jnz"]:
        return 2
    elif operator in ["mov", "and", "or", "xor", "add", "sub", "mul", "div", "mod", "shl", "cmp", "lt", "load", "store"]:
        return 3
    else:
        raise Exception(f"unknown instruction \"{operator}\"")


def find_symbols(lines: List[Line]) -> SymbolTable:
    symbols = SymbolTableBuilder()
    lc = 0
    for line in lines:
        if line.label:
            if line.label.startswith("."):
                symbols.define_local(line.label, lc)
            else:
                symbols.define_global(line.label, lc)
        if line.operation:
            lc += instruction_size(line.operation.operator)
    return symbols.build()
