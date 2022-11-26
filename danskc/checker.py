from __future__ import annotations
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple, cast
from parser_ import (
    ParsedBreak,
    ParsedIdType,
    ParsedParam,
    ParsedStatementTypes,
    ParsedStatement,
    ParsedExprStatement,
    ParsedLet,
    ParsedIf,
    ParsedType,
    ParsedTypeTypes,
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


class CheckedExprStatement(CheckedStatement):
    def __init__(self, value: CheckedExpr) -> None:
        super().__init__()
        self.value = value

    def statement_type(self) -> CheckedStatementTypes:
        return CheckedStatementTypes.Expr


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


class CheckedIf(CheckedStatement):
    def __init__(
        self,
        condition: CheckedExpr,
        truthy: List[CheckedStatement],
        falsy: List[CheckedStatement],
    ) -> None:
        super().__init__()
        self.condition = condition
        self.truthy = truthy
        self.falsy = falsy

    def statement_type(self) -> CheckedStatementTypes:
        return CheckedStatementTypes.If


class CheckedWhile(CheckedStatement):
    def __init__(self, condition: CheckedExpr, body: List[CheckedStatement]) -> None:
        super().__init__()
        self.condition = condition
        self.body = body

    def statement_type(self) -> CheckedStatementTypes:
        return CheckedStatementTypes.While


class CheckedBreak(CheckedStatement):
    def __init__(self) -> None:
        super().__init__()

    def statement_type(self) -> CheckedStatementTypes:
        return CheckedStatementTypes.Break


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
        return CheckedStatementTypes.Func


class CheckedReturn(CheckedStatement):
    def __init__(self, value: Optional[CheckedExpr]) -> None:
        super().__init__()
        self.value = value

    def statement_type(self) -> CheckedStatementTypes:
        return CheckedStatementTypes.Return


class CheckedParam:
    def __init__(self, subject: str, value_type: CheckedType) -> None:
        self.subject = subject
        self.value_type = value_type


class CheckedTypeTypes(Enum):
    Int = auto()
    Float = auto()
    Char = auto()
    String = auto()
    Bool = auto()
    Array = auto()
    Object = auto()
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


class CheckedFloatType(CheckedType):
    def __init__(self) -> None:
        super().__init__()

        def type_type(self) -> CheckedTypeTypes:
            return CheckedTypeTypes.Float


class CheckedCharType(CheckedType):
    def __init__(self) -> None:
        super().__init__()

        def type_type(self) -> CheckedTypeTypes:
            return CheckedTypeTypes.Char


class CheckedStringType(CheckedType):
    def __init__(self) -> None:
        super().__init__()

        def type_type(self) -> CheckedTypeTypes:
            return CheckedTypeTypes.String


class CheckedBoolType(CheckedType):
    def __init__(self) -> None:
        super().__init__()

        def type_type(self) -> CheckedTypeTypes:
            return CheckedTypeTypes.Bool


class CheckedArrayType(CheckedType):
    def __init__(self, inner_type: CheckedType) -> None:
        super().__init__()
        self.inner_type = inner_type

        def type_type(self) -> CheckedTypeTypes:
            return CheckedTypeTypes.Array


class CheckedObjectType(CheckedType):
    def __init__(self, fields: List[CheckedParam]) -> None:
        super().__init__()
        self.fields = fields

        def type_type(self) -> CheckedTypeTypes:
            return CheckedTypeTypes.Object


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

    def expr_value_type(self) -> CheckedType:
        raise NotImplementedError()


class CheckedId(CheckedExpr):
    def __init__(self, value: str, symbol_id: int, value_type: CheckedType) -> None:
        super().__init__()
        self.value = value
        self.symbol_id = symbol_id
        self.value_type = value_type

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Id

    def expr_value_type(self) -> CheckedType:
        return self.value_type


class CheckedInt(CheckedExpr):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Int

    def expr_value_type(self) -> CheckedType:
        return CheckedIntType()


class CheckedFloat(CheckedExpr):
    def __init__(self, value: float) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Float

    def expr_value_type(self) -> CheckedType:
        return CheckedFloatType()


class CheckedChar(CheckedExpr):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Char

    def expr_value_type(self) -> CheckedType:
        return CheckedCharType()


class CheckedString(CheckedExpr):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.String

    def expr_value_type(self) -> CheckedType:
        return CheckedStringType()


class CheckedBool(CheckedExpr):
    def __init__(self, value: bool) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Bool

    def expr_value_type(self) -> CheckedType:
        return CheckedBoolType()


class CheckedArray(CheckedExpr):
    def __init__(self, values: List[CheckedExpr], value_type: CheckedArrayType) -> None:
        super().__init__()
        self.values = values
        self.value_type = value_type

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Array

    def expr_value_type(self) -> CheckedType:
        return self.value_type


class CheckedObject(CheckedExpr):
    def __init__(
        self,
        values: List[Tuple[str, CheckedExpr]],
        value_type: CheckedObjectType,
    ) -> None:
        super().__init__()
        self.values = values
        self.value_type = value_type

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Object

    def expr_value_type(self) -> CheckedType:
        return self.value_type


class CheckedAccessing(CheckedExpr):
    def __init__(
        self,
        subject: CheckedExpr,
        value: str,
        value_type: CheckedObjectType,
    ) -> None:
        super().__init__()
        self.subject = subject
        self.value = value
        self.value_type = value_type

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Accessing

    def expr_value_type(self) -> CheckedType:
        return self.value_type


class CheckedIndexing(CheckedExpr):
    def __init__(
        self,
        subject: CheckedExpr,
        value: CheckedExpr,
        value_type: CheckedObjectType,
    ) -> None:
        super().__init__()
        self.subject = subject
        self.value = value
        self.value_type = value_type

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Indexing

    def expr_value_type(self) -> CheckedType:
        return self.value_type


class CheckedCall(CheckedExpr):
    def __init__(
        self,
        subject: CheckedExpr,
        args: List[CheckedExpr],
        value_type: CheckedType,
    ) -> None:
        super().__init__()
        self.subject = subject
        self.args = args
        self.value_type = value_type

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Call

    def expr_value_type(self) -> CheckedType:
        return self.value_type


class CheckedUnaryOperations(Enum):
    Not = auto()


class CheckedUnary(CheckedExpr):
    def __init__(
        self,
        subject: CheckedExpr,
        operation: CheckedUnaryOperations,
        value_type: CheckedObjectType,
    ) -> None:
        super().__init__()
        self.subject = subject
        self.operation = operation
        self.value_type = value_type

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Unary

    def expr_value_type(self) -> CheckedType:
        return self.value_type


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
        self,
        left: CheckedExpr,
        right: CheckedExpr,
        operation: CheckedBinaryOperations,
        value_type: CheckedObjectType,
    ) -> None:
        super().__init__()
        self.left = left
        self.right = right
        self.operation = operation
        self.value_type = value_type

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Binary

    def expr_value_type(self) -> CheckedType:
        return self.value_type


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
        value_type: CheckedObjectType,
    ) -> None:
        super().__init__()
        self.subject = subject
        self.value = value
        self.operation = operation
        self.value_type = value_type

    def expr_type(self) -> CheckedExprTypes:
        return CheckedExprTypes.Assign

    def expr_value_type(self) -> CheckedType:
        return self.value_type


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

    def define(self, subject: str, value_type: CheckedType) -> None:
        if subject in self.table:
            raise Exception(
                f'shouldn\'t be possible, but multiple declarations of symbol "{subject}"'
            )
        else:
            self.table[subject] = value_type

    def has(self, subject: str) -> bool:
        return subject in self.table or subject in self.decl_locations

    def get(self, subject: str) -> CheckedType:
        if subject in self.table:
            return self.table[subject]
        else:
            if subject in self.decl_locations:
                raise NotImplementedError()
            else:
                raise Exception(f'use of undefined/indeclared symbol "{subject}"')


class GlobalTableBuilder:
    def __init__(self) -> None:
        self.table: Dict[str, int] = {}

    def declare(self, subject: str, index: int) -> None:
        if subject in self.table:
            raise Exception(f'multiple declarations of symbol "{subject}"')
        self.table[subject] = index

    def build(self, top_level: List[ParsedStatement]) -> GlobalTable:
        return GlobalTable(top_level, self.table)


class LocalTable:
    def __init__(self) -> None:
        pass

    def __add_symbol(self, subject: str, value_type: CheckedType) -> int:
        pass

    def define(self, subject: str, value_type: CheckedType) -> int:
        raise NotImplementedError()

    def has(self, subject: str) -> bool:
        raise NotImplementedError()

    def get(self, subject: str) -> CheckedType:
        raise NotImplementedError()

    def branch(self) -> LocalTable:
        raise NotImplementedError()

    def return_type_compatible(self, other: CheckedType) -> bool:
        raise NotImplementedError()


class TopLevelLocalTable(LocalTable):
    def __init__(self, global_table: GlobalTable, return_type: CheckedType) -> None:
        self.global_table = global_table
        self.table: List[Tuple[str, CheckedType]] = []
        self.local_symbols: Dict[str, CheckedType] = {}
        self.return_type = return_type

    def __add_symbol(self, subject: str, value_type: CheckedType) -> int:
        self.table.append((subject, value_type))
        return len(self.table) - 1

    def define(self, subject: str, value_type: CheckedType) -> int:
        if subject in self.local_symbols:
            raise Exception(f'multiple definitions of symbol "{subject}"')
        self.local_symbols[subject] = value_type
        return self.__add_symbol(subject, value_type)

    def has(self, subject: str) -> bool:
        return subject in self.local_symbols or self.global_table.has(subject)

    def get(self, subject: str) -> CheckedType:
        if subject in self.local_symbols:
            return self.local_symbols[subject]
        elif self.global_table.has(subject):
            return self.global_table.get(subject)
        else:
            raise Exception(f'use of undefined symbol "{subject}"')

    def branch(self) -> LocalTable:
        return BranchedLocalTable(self)

    def return_type_compatible(self, other: CheckedType) -> bool:
        return types_compatible(self.return_type, other)


class BranchedLocalTable(LocalTable):
    def __init__(self, parent: LocalTable) -> None:
        self.parent = parent
        self.table: Dict[str, CheckedType] = {}

    def __add_symbol(self, subject: str, value_type: CheckedType) -> int:
        return self.parent.__add_symbol(subject, value_type)

    def define(self, subject: str, value_type: CheckedType) -> int:
        if subject in self.table:
            raise Exception(f'multiple definitions of symbol "{subject}"')
        self.table[subject] = value_type
        return self.__add_symbol(subject, value_type)

    def has(self, subject: str) -> bool:
        return subject in self.table or self.parent.has(subject)

    def get(self, subject: str) -> CheckedType:
        if subject in self.table:
            return self.table[subject]
        elif self.parent.has(subject):
            return self.parent.get(subject)
        else:
            raise Exception(f'use of undefined symbol "{subject}"')

    def branch(self) -> LocalTable:
        return BranchedLocalTable(self)

    def return_type_compatible(self, other: CheckedType) -> bool:
        return self.parent.return_type_compatible(other)


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
            raise Exception(
                f"statement {statement.statement_type()} not allowed in top level"
            )
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
    value = check_top_level_expr(node.value, global_table)
    return CheckedLet(node.subject, value_type, value)


def check_top_level_expr(node: ParsedExpr, global_table: GlobalTable) -> CheckedExpr:
    if node.expr_type() == CheckedExprTypes.Int:
        int_node = cast(CheckedInt, node)
        return CheckedInt(int_node.value)
    else:
        raise NotImplementedError()


def check_top_level_func(node: ParsedFunc, global_table: GlobalTable) -> CheckedFunc:
    params = [CheckedParam(p.subject, check_type(p.value_type)) for p in node.params]
    return_type = check_type(node.return_type)
    local_table = TopLevelLocalTable(global_table, return_type)
    for param in params:
        local_table.define(param.subject, param.value_type)
    global_table.define(node.subject, CheckedFuncType(params, return_type))
    body = check_statements(node.body, local_table.branch())
    return CheckedFunc(node.subject, params, return_type, body)


def check_statements(
    nodes: List[ParsedStatement],
    local_table: LocalTable,
) -> List[CheckedStatement]:
    return [check_statement(node, local_table) for node in nodes]


def check_statement(
    node: ParsedStatement,
    local_table: LocalTable,
) -> CheckedStatement:
    if node.statement_type() == ParsedStatementTypes.Expr:
        return check_expr_statement(cast(ParsedExprStatement, node), local_table)
    elif node.statement_type() == ParsedStatementTypes.Let:
        return check_let(cast(ParsedLet, node), local_table)
    elif node.statement_type() == ParsedStatementTypes.If:
        return check_if(cast(ParsedIf, node), local_table)
    elif node.statement_type() == ParsedStatementTypes.While:
        return check_while(cast(ParsedWhile, node), local_table)
    elif node.statement_type() == ParsedStatementTypes.Break:
        return check_break(cast(ParsedBreak, node), local_table)
    elif node.statement_type() == ParsedStatementTypes.Func:
        return check_func(cast(ParsedFunc, node), local_table)
    elif node.statement_type() == ParsedStatementTypes.Return:
        return check_return(cast(ParsedReturn, node), local_table)
    else:
        raise Exception(f"unknown statement {node.statement_type()}")


def check_expr_statement(
    node: ParsedExprStatement,
    local_table: LocalTable,
) -> CheckedExprStatement:
    return CheckedExprStatement(check_expr(node.value, local_table))


def check_let(node: ParsedLet, local_table: LocalTable) -> CheckedLet:
    value_type = check_type(node.value_type)
    local_table.define(node.subject, value_type)
    value = check_expr(node.value, local_table)
    return CheckedLet(node.subject, value_type, value)


def check_if(node: ParsedIf, local_table: LocalTable) -> CheckedIf:
    return CheckedIf(
        check_expr(node.condition, local_table),
        check_statements(node.truthy, local_table),
        check_statements(node.falsy, local_table),
    )


def check_while(node: ParsedWhile, local_table: LocalTable) -> CheckedWhile:
    return CheckedWhile(
        check_expr(node.condition, local_table),
        check_statements(node.body, local_table),
    )


def check_break(node: ParsedBreak, local_table: LocalTable) -> CheckedBreak:
    return CheckedBreak()


def check_func(node: ParsedFunc, local_table: LocalTable) -> CheckedFunc:
    raise Exception("func statements are only legal in top level")


def check_return(node: ParsedReturn, local_table: LocalTable) -> CheckedReturn:
    if node.value:
        return CheckedReturn(check_expr(node.value, local_table))
    else:
        return CheckedReturn(None)


def check_type(node: ParsedType) -> CheckedType:
    if node.type_type() == ParsedTypeTypes.Id:
        return check_id_type(cast(ParsedIdType, node))
    else:
        raise Exception(f"unimplemented/unknown type {node.type_type()}")


def check_id_type(node: ParsedIdType) -> CheckedType:
    if node.value == "heltal":
        return CheckedIntType()
    elif node.value == "decimal":
        return CheckedFloatType()
    elif node.value == "tegn":
        return CheckedCharType()
    elif node.value == "tekst":
        return CheckedStringType()
    else:
        raise Exception(f"unknown type id {node.value}")


def types_compatible(a: CheckedType, b: CheckedType) -> bool:
    if a.type_type() == ParsedTypeTypes.Id and b.type_type() == ParsedTypeTypes.Id:
        id_a = cast(ParsedIdType, a)
        id_b = cast(ParsedIdType, b)
        return id_a.value == id_b.value
    else:
        raise Exception(
            f"incompatible/unimplemented compatibility between types {a.type_type()} and {b.type_type()}"
        )


def check_expr(node: ParsedExpr, local_table: LocalTable) -> CheckedExpr:
    if node.expr_type() == ParsedExprTypes.Id:
        return check_id(cast(ParsedId, node), local_table)
    elif node.expr_type() == ParsedExprTypes.Int:
        return CheckedInt(cast(ParsedInt, node).value)
    elif node.expr_type() == ParsedExprTypes.Float:
        return CheckedFloat(cast(ParsedFloat, node).value)
    elif node.expr_type() == ParsedExprTypes.Char:
        return CheckedChar(cast(ParsedChar, node).value)
    elif node.expr_type() == ParsedExprTypes.String:
        return CheckedString(cast(ParsedString, node).value)
    elif node.expr_type() == ParsedExprTypes.Bool:
        return CheckedBool(cast(ParsedBool, node).value)
    elif node.expr_type() == ParsedExprTypes.Array:
        return check_array(cast(ParsedArray, node), local_table)
    elif node.expr_type() == ParsedExprTypes.Object:
        return check_object(cast(ParsedObject, node), local_table)
    elif node.expr_type() == ParsedExprTypes.Accessing:
        return check_accessing(cast(ParsedAccessing, node), local_table)
    elif node.expr_type() == ParsedExprTypes.Indexing:
        return check_indexing(cast(ParsedIndexing, node), local_table)
    elif node.expr_type() == ParsedExprTypes.Call:
        return check_call(cast(ParsedCall, node), local_table)
    elif node.expr_type() == ParsedExprTypes.Unary:
        return check_unary(cast(ParsedUnary, node), local_table)
    elif node.expr_type() == ParsedExprTypes.Binary:
        return check_binary(cast(ParsedBinary, node), local_table)
    elif node.expr_type() == ParsedExprTypes.Assign:
        return check_assign(cast(ParsedAssign, node), local_table)
    else:
        raise Exception(f"unknown expression {node.expr_type()}")


def check_id(node: ParsedId, local_table: LocalTable) -> CheckedId:
    raise NotImplementedError()


def check_array(node: ParsedArray, local_table: LocalTable) -> CheckedArray:
    checked_values = [check_expr(value, local_table) for value in node.values]
    if len(checked_values) == 0:
        raise Exception("empty arrays are unimplemented")
    return CheckedArray(
        checked_values, CheckedArrayType(checked_values[0].expr_value_type())
    )


def check_object(node: ParsedObject, local_table: LocalTable) -> CheckedObject:
    used_keys: List[str] = []
    checked_values: List[Tuple[str, CheckedExpr]] = []
    checked_params: List[CheckedParam] = []
    for (key, value) in node.values:
        if key in used_keys:
            raise Exception("cannot reuse key in object")
        used_keys.append(key)
        checked_value = check_expr(value, local_table)
        checked_values.append((key, checked_value))
        checked_params.append(CheckedParam(key, checked_value.expr_value_type()))
    return CheckedObject(checked_values, CheckedObjectType(checked_params))


def check_accessing(node: ParsedAccessing, local_table: LocalTable) -> CheckedAccessing:
    raise NotImplementedError()


def check_indexing(node: ParsedIndexing, local_table: LocalTable) -> CheckedIndexing:
    raise NotImplementedError()


def check_call(node: ParsedCall, local_table: LocalTable) -> CheckedCall:
    checked_subject = check_expr(node.subject, local_table)
    if checked_subject.expr_value_type().type_type() != CheckedTypeTypes.Func:
        raise Exception("expression is not callable")
    subject_type = cast(CheckedFuncType, checked_subject.expr_type())
    checked_args = [check_expr(arg, local_table) for arg in node.args]
    if len(subject_type.params) != len(checked_args):
        raise Exception("wrong number of arguments")
    for i in range(len(subject_type.params)):
        if (
            checked_args[i].expr_value_type().type_type()
            != subject_type.params[i].value_type.type_type()
        ):
            raise Exception(f"argument nr. {i + 1} is invalid")
    return CheckedCall(
        checked_subject,
        checked_args,
        subject_type.return_type,
    )


def check_unary(node: ParsedUnary, local_table: LocalTable) -> CheckedUnary:
    raise NotImplementedError()


def check_binary(node: ParsedBinary, local_table: LocalTable) -> CheckedBinary:
    raise NotImplementedError()


def check_assign(node: ParsedAssign, local_table: LocalTable) -> CheckedAssign:
    raise NotImplementedError()
