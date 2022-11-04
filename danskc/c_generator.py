from __future__ import annotations
from collections import namedtuple
from typing import Dict, List, Tuple, cast
from parser_ import (
    StatementType,
    Statement,
    ExprStatement,
    Let,
    If,
    While,
    Return,
    ExprType,
    Expr,
    Func,
    Id,
    Int,
    Float,
    Char,
    String,
    Bool,
    Array,
    Object,
    Accessing,
    Indexing,
    Call,
    UnaryOperations,
    Unary,
    BinaryOperations,
    Binary,
    AssignOperations,
    Assign,
)


class GlobalTable:
    def __init__(self, decl_indices: Dict[str, int]) -> None:
        self.decl_indices = decl_indices


class GlobalTableBuilder:
    def __init__(self) -> None:
        self.indices: Dict[str, int] = {}

    def declare_let_at(self, i: int, node: Let) -> None:
        if node.subject in self.indices:
            raise Exception(f'multiple definitions of symbol "{node.subject}"')
        self.indices[node.subject] = i

    def declare_func_at(self, i: int, node: Func) -> None:
        if node.subject in self.indices:
            raise Exception(f'multiple definitions of symbol "{node.subject}"')
        self.indices[node.subject] = i

    def build(self) -> GlobalTable:
        return GlobalTable(self.indices)


def build_global_table(ast: List[Statement]) -> GlobalTable:
    table = GlobalTableBuilder()
    for i, statement in enumerate(ast):
        if statement.statement_type() == StatementType.Func:
            table.declare_func_at(i, cast(Func, statement))
        elif statement.statement_type() == StatementType.Let:
            table.declare_let_at(i, cast(Let, statement))
    return table.build()


def generate_program(ast: List[Statement]) -> str:
    global_table = build_global_table(ast)
    return "int main(){((int*)0)=0;}"
