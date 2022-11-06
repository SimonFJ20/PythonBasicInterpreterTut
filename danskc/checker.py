from __future__ import annotations
from enum import Enum, auto
from typing import Dict, List, Tuple, cast
from parser_ import (
    ParsedParam,
    ParsedStatementTypes,
    ParsedStatement,
    ParsedExprStatement,
    ParsedLet,
    ParsedIf,
    ParsedType,
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


class CheckedStatementTypes(Enum):
    Expr = auto()
    Let = auto()
    If = auto()
    While = auto()
    Break = auto()
    Func = auto()
    Return = auto()


class CheckedStatement:
    def __init__(self) -> None:
        pass

    def statement_type(self) -> CheckedStatementTypes:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()


class CheckedLet(CheckedStatement):
    def __init__(
        self, subject: str, value_type: CheckedType, value: CheckedExpr
    ) -> None:
        super().__init__()
        self.subject = subject
        self.value_type = value_type
        self.value = value

    def statement_type(self) -> CheckedStatementTypes:
        return CheckedStatementTypes.Let


class CheckedFunc(CheckedStatement):
    def __init__(
        self,
        subject: str,
        params: List[CheckedParam],
        return_type: CheckedType,
        body: List[CheckedStatement],
    ) -> None:
        super().__init__()
        self.subject = subject
        self.params = params
        self.return_type = return_type
        self.body = body

    def statement_type(self) -> CheckedStatementTypes:
        return CheckedStatementTypes.While


class CheckedParam:
    def __init__(self, subject: str, value_type: CheckedType) -> None:
        self.subject = subject
        self.value_type = value_type


class CheckedTypeTypes(Enum):
    Int = auto()
    Func = auto()


class CheckedType:
    def __init__(self) -> None:
        pass

    def type_type(self) -> CheckedTypeTypes:
        raise NotImplementedError()


class CheckedIntType(CheckedType):
    def __init__(self) -> None:
        super().__init__()

    def type_type(self) -> CheckedTypeTypes:
        return CheckedTypeTypes.Int


class CheckedFuncType(CheckedType):
    def __init__(self, params: List[CheckedParam], return_type: CheckedType) -> None:
        super().__init__()
        self.params = params
        self.return_type = return_type

    def type_type(self) -> CheckedTypeTypes:
        return CheckedTypeTypes.Func


def check_program(ast: List[ParsedStatement]) -> List[CheckedStatement]:
    pass


class CheckedExprTypes(Enum):
    Id = auto()
    Int = auto()
    Float = auto()
    Char = auto()
    String = auto()
    Bool = auto()
    Array = auto()
    Object = auto()
    Accessing = auto()
    Indexing = auto()
    Call = auto()
    Unary = auto()
    Binary = auto()
    Assign = auto()


class CheckedExpr:
    def __init__(self) -> None:
        pass

    def expr_type(self) -> CheckedExprTypes:
        raise NotImplementedError()


class CheckedId(CheckedExpr):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Id


class CheckedInt(CheckedExpr):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Int


class CheckedFloat(CheckedExpr):
    def __init__(self, value: float) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Float


class CheckedChar(CheckedExpr):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Char


class CheckedString(CheckedExpr):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.String


class CheckedBool(CheckedExpr):
    def __init__(self, value: bool) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Bool


class CheckedArray(CheckedExpr):
    def __init__(self, values: List[CheckedExpr]) -> None:
        super().__init__()
        self.values = values

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Array


class CheckedObject(CheckedExpr):
    def __init__(self, values: List[Tuple[str, CheckedExpr]]) -> None:
        super().__init__()
        self.values = values

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Object


class CheckedAccessing(CheckedExpr):
    def __init__(self, subject: CheckedExpr, value: str) -> None:
        super().__init__()
        self.subject = subject
        self.value = value

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Accessing


class CheckedIndexing(CheckedExpr):
    def __init__(self, subject: CheckedExpr, value: CheckedExpr) -> None:
        super().__init__()
        self.subject = subject
        self.value = value

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Indexing


class CheckedCall(CheckedExpr):
    def __init__(self, subject: CheckedExpr, args: List[CheckedExpr]) -> None:
        super().__init__()
        self.subject = subject
        self.args = args

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Call


class CheckedUnaryOperations(Enum):
    Not = auto()


class CheckedUnary(CheckedExpr):
    def __init__(self, subject: CheckedExpr, operation: CheckedUnaryOperations) -> None:
        super().__init__()
        self.subject = subject
        self.operation = operation

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Unary


class CheckedBinaryOperations(Enum):
    Add = auto()
    Subtract = auto()
    Multiply = auto()
    EQ = auto()
    NE = auto()
    LT = auto()
    LTE = auto()
    GT = auto()
    GTE = auto()


class CheckedBinary(CheckedExpr):
    def __init__(
        self, left: CheckedExpr, right: CheckedExpr, operation: CheckedBinaryOperations
    ) -> None:
        super().__init__()
        self.left = left
        self.right = right
        self.operation = operation

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Binary


class CheckedAssignOperations(Enum):
    Assign = auto()
    Increment = auto()
    Decrement = auto()


class CheckedAssign(CheckedExpr):
    def __init__(
        self,
        subject: CheckedExpr,
        value: CheckedExpr,
        operation: CheckedAssignOperations,
    ) -> None:
        super().__init__()
        self.subject = subject
        self.value = value
        self.operation = operation

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Assign


class GlobalSymbol:
    def __init__(self) -> None:
        pass


class GlobalTable:
    def __init__(
        self, top_level: List[ParsedStatement], decl_locations: Dict[str, int]
    ) -> None:
        self.top_level = top_level
        self.decl_locations = decl_locations
        self.table: Dict[str, CheckedType] = {}

    def get(self, subject: str) -> CheckedType:
        if subject in self.table:
            return self.table[subject]
        else:
            if subject in self.decl_locations:
                raise NotImplementedError()
            else:
                raise Exception(f'use of undefined/indeclared symbol "{subject}"')

    def define(self, subject: str, value_type: CheckedType) -> None:
        if subject in self.table:
            raise Exception(
                f'shouldn\'t be possible, but multiple declarations of symbol "{subject}"'
            )
        else:
            self.table[subject] = value_type


class GlobalTableBuilder:
    def __init__(self) -> None:
        self.table: Dict[str, int] = {}

    def declare(self, subject: str, index: int) -> None:
        if subject in self.table:
            raise Exception(f'multiple declarations of symbol "{subject}"')
        self.table[subject] = index

    def build(self, top_level: List[ParsedStatement]) -> GlobalTable:
        return GlobalTable(top_level, self.table)


def check_top_level_statements(
    top_level: List[ParsedStatement],
) -> List[CheckedStatement]:
    global_table = build_global_table(top_level)
    checked_statements: List[CheckedStatement] = []
    for statement in top_level:
        if statement.statement_type() == ParsedStatementTypes.Let:
            let = cast(ParsedLet, statement)
            checked_statements.append(check_top_level_let(let, global_table))
        elif statement.statement_type() == ParsedStatementTypes.Func:
            func = cast(ParsedFunc, statement)
            checked_statements.append(check_top_level_func(func, global_table))
        else:
            raise Exception(f"statement {statement} not allowed in top level")
    return checked_statements


def build_global_table(top_level: List[ParsedStatement]) -> GlobalTable:
    global_table = GlobalTableBuilder()
    for i, statement in enumerate(top_level):
        if statement.statement_type() == ParsedStatementTypes.Let:
            let = cast(ParsedLet, statement)
            global_table.declare(let.subject, i)
        elif statement.statement_type() == ParsedStatementTypes.Func:
            func = cast(ParsedFunc, statement)
            global_table.declare(func.subject, i)
    return global_table.build(top_level)


def check_top_level_let(node: ParsedLet, global_table: GlobalTable) -> CheckedLet:
    value_type = check_type(node.value_type)
    global_table.define(node.subject, value_type)
    value = check_top_level_expr(node.value)
    return CheckedLet(node.subject, value_type, value)


def check_top_level_expr(node: ParsedExpr) -> CheckedExpr:
    if node.expr_type() == CheckedExprTypes.Int:
        int_node = cast(CheckedInt, node)
        return CheckedInt(int_node.value)
    else:
        raise NotImplementedError()


def check_top_level_func(node: ParsedFunc, global_table: GlobalTable) -> CheckedFunc:
    params = [CheckedParam(p.subject, check_type(p.value_type)) for p in node.params]
    return_type = check_type(node.return_type)
    global_table.define(node.subject, CheckedFuncType(params, return_type))
    body = check_statements(node.body)
    return CheckedFunc(node.subject, params, return_type, body)


def check_statements(node: List[ParsedStatement]) -> List[CheckedStatement]:
    pass


def check_type(type: ParsedType) -> CheckedType:
    pass
