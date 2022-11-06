from __future__ import annotations
from enum import Enum, auto
from typing import Dict, List, Tuple, cast
from parser_ import (
    ParsedStatementTypes,
    ParsedStatement,
    ParsedExprStatement,
    ParsedLet,
    ParsedIf,
    ParsedWhile,
    ParsedReturn,
    ParsedExprTypes,
    ParsedExpr,
    ParsedFunc,
    ParsedId,
    ParsedInt,
    ParsedFloat,
    ParsedChar,
    ParsedString,
    ParsedBool,
    ParsedArray,
    ParsedObject,
    ParsedAccessing,
    ParsedIndexing,
    ParsedCall,
    ParsedUnaryOperations,
    ParsedUnary,
    ParsedBinaryOperations,
    ParsedBinary,
    ParsedAssignOperations,
    ParsedAssign,
)


class GlobalTable:
    def __init__(self, decl_indices: Dict[str, int]) -> None:
        self.decl_indices = decl_indices


class GlobalTableBuilder:
    def __init__(self) -> None:
        self.indices: Dict[str, int] = {}

    def declare_let_at(self, i: int, node: ParsedLet) -> None:
        if node.subject in self.indices:
            raise Exception(f'multiple definitions of symbol "{node.subject}"')
        self.indices[node.subject] = i

    def declare_func_at(self, i: int, node: ParsedFunc) -> None:
        if node.subject in self.indices:
            raise Exception(f'multiple definitions of symbol "{node.subject}"')
        self.indices[node.subject] = i

    def build(self) -> GlobalTable:
        return GlobalTable(self.indices)


def build_global_table(ast: List[ParsedStatement]) -> GlobalTable:
    table = GlobalTableBuilder()
    for i, statement in enumerate(ast):
        if statement.statement_type() == ParsedStatementTypes.Let:
            table.declare_let_at(i, cast(ParsedLet, statement))
        elif statement.statement_type() == ParsedStatementTypes.Func:
            table.declare_func_at(i, cast(ParsedFunc, statement))
    return table.build()


def generate_program(ast: List[ParsedStatement]) -> str:
    global_table = build_global_table(ast)
    return "int main(){*((int*)0)=0;}"


def generate_top_level_statements(
    nodes: List[ParsedStatement], global_table: GlobalTable
) -> str:
    return "\n\n".join(
        [generate_top_level_statement(node, global_table) for node in nodes]
    )


def generate_top_level_statement(node: ParsedStatement, global_table: GlobalTable) -> str:
    if node.statement_type() == ParsedStatementTypes.Let:
        return generate_top_level_let(cast(ParsedLet, node), global_table)
    elif node.statement_type() == ParsedStatementTypes.Func:
        return generate_top_level_func(cast(ParsedFunc, node), global_table)
    else:
        raise Exception(
            f"statement type {node.statement_type()} not allowed in top level"
        )


def generate_top_level_let(node: ParsedLet, global_table: GlobalTable) -> str:
    raise NotImplementedError()

class TypeType(Enum):
    Name = auto(),

class Type:
    def __init__(self) -> None:
        pass

    def type_type(self) -> TypeType:
        raise NotImplementedError()

    def is_compatible(self, other: Type) -> bool:
        raise NotImplementedError()

class NameType(Type):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def type_type(self) -> TypeType:
        return TypeType.Name

    def is_compatible(self, other: Type) -> bool:
        if other.type_type() == TypeType.Name:
            return cast(NameType, other).value == self.value
        else:
            raise NotImplementedError()

class Local:
    def __init__(self, name: str, valuetype: Type, scopedepth: int) -> None:
        self.name = name
        self.valuetype = valuetype
        self.scopedepth = scopedepth

class LocalTable:
    def __init__(self, global_table: GlobalTable) -> None:
        self.global_table = global_table
        self.local_table: Dict[str, Local] = {}
        self.depth = 0

    def define_local(self, name: str, valuetype: Type) -> None:
        if name in self.local_table and self.local_table[name].scopedepth == self.depth:
            raise Exception(f'multiple definitions of local "{name}"')

def generate_top_level_func(node: ParsedFunc, global_table: GlobalTable) -> str:

