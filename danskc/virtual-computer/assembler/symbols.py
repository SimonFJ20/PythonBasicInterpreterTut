from typing import Dict, List, Optional, cast
from assembler.parser import Line
from assembler.spec import PROGRAM_START, instruction_size

class SymbolTable:
    def __init__(self, global_symbols: Dict[str, int], local_symbols: Dict[str, List[int]]) -> None:
        self.global_symbols = global_symbols
        self.local_symbols = local_symbols

    def is_defined(self, name: str) -> bool:
        return name in self.global_symbols or name in self.local_symbols
    
    def get(self, name: str, lc: int) -> int:
        assert self.is_defined(name)
        if name.startswith("."):
            closest: Optional[int] = None
            for l in self.local_symbols[name]:
                if not closest or abs(closest - lc) > abs(l - lc):
                    closest = l
            assert closest != None
            return cast(int, closest)    
        else:
            return self.global_symbols[name]

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

def find_symbols(lines: List[Line]) -> SymbolTable:
    symbols = SymbolTableBuilder()
    lc = PROGRAM_START
    for line in lines:
        if line.label:
            if line.label.startswith("."):
                symbols.define_local(line.label, lc)
            else:
                symbols.define_global(line.label, lc)
        if line.operation:
            lc += instruction_size(line.operation.operator)
    return symbols.build()
