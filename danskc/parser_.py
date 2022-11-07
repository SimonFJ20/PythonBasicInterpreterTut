from __future__ import annotations
from enum import Enum, auto
from typing import Any, List, Optional, Tuple
from tokenizer import Token, TokenTypes


class ParsedStatementTypes(Enum):
    Expr = auto()
    Let = auto()
    If = auto()
    While = auto()
    Break = auto()
    Func = auto()
    Return = auto()


class ParsedStatement:
    def __init__(self) -> None:
        pass

    def statement_type(self) -> ParsedStatementTypes:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()


def parsed_statements_to_string(statements: List[ParsedStatement]) -> str:
    statements_ = "\n".join(str(statement) for statement in statements)
    return f"[ {statements_} ]"


class ParsedExprStatement(ParsedStatement):
    def __init__(self, value: ParsedExpr) -> None:
        super().__init__()
        self.value = value

    def statement_type(self) -> ParsedStatementTypes:
        return ParsedStatementTypes.Expr

    def __str__(self) -> str:
        return f"ExprStatement {{ value: {self.value} }}"


class ParsedLet(ParsedStatement):
    def __init__(self, subject: str, value_type: ParsedType, value: ParsedExpr) -> None:
        super().__init__()
        self.subject = subject
        self.value_type = value_type
        self.value = value

    def statement_type(self) -> ParsedStatementTypes:
        return ParsedStatementTypes.Let

    def __str__(self) -> str:
        return f"Let {{ subject: {self.subject}, value: {self.value} }}"


class ParsedIf(ParsedStatement):
    def __init__(
        self,
        condition: ParsedExpr,
        truthy: List[ParsedStatement],
        falsy: List[ParsedStatement],
    ) -> None:
        super().__init__()
        self.condition = condition
        self.truthy = truthy
        self.falsy = falsy

    def statement_type(self) -> ParsedStatementTypes:
        return ParsedStatementTypes.If

    def __str__(self) -> str:
        truthy = ", ".join(str(statement) for statement in self.truthy)
        falsy = ", ".join(str(statement) for statement in self.falsy)
        return f"If {{ condition: {self.condition}, truthy: [ {truthy} ], falsy: [ {falsy} ] }}"


class ParsedWhile(ParsedStatement):
    def __init__(self, condition: ParsedExpr, body: List[ParsedStatement]) -> None:
        super().__init__()
        self.condition = condition
        self.body = body

    def statement_type(self) -> ParsedStatementTypes:
        return ParsedStatementTypes.While

    def __str__(self) -> str:
        body = ", ".join(str(statement) for statement in self.body)
        return f"If {{ condition: {self.condition}, body: [ {body} ] }}"


class ParsedBreak(ParsedStatement):
    def __init__(self) -> None:
        super().__init__()

    def statement_type(self) -> ParsedStatementTypes:
        return ParsedStatementTypes.Break

    def __str__(self) -> str:
        return f"Break"


class ParsedFunc(ParsedStatement):
    def __init__(
        self,
        subject: str,
        params: List[ParsedParam],
        return_type: ParsedType,
        body: List[ParsedStatement],
    ) -> None:
        super().__init__()
        self.subject = subject
        self.params = params
        self.return_type = return_type
        self.body = body

    def statement_type(self) -> ParsedStatementTypes:
        return ParsedStatementTypes.Func

    def __str__(self) -> str:
        params = ", ".join(str(param) for param in self.params)
        body = ", ".join(str(statement) for statement in self.body)
        return f"""Func {{
            subject: {self.subject},
            params: [ {params} ],
            return_type: {self.return_type},
            body: [ {body} ]
        }}"""


class ParsedReturn(ParsedStatement):
    def __init__(self, value: Optional[ParsedExpr]) -> None:
        super().__init__()
        self.value = value

    def statement_type(self) -> ParsedStatementTypes:
        return ParsedStatementTypes.Return

    def __str__(self) -> str:
        return f"Return {{ value: {self.value} }}"


class ParsedTypeTypes(Enum):
    Id = auto()


class ParsedParam:
    def __init__(self, subject: str, value_type: ParsedType) -> None:
        self.subject = subject
        self.value_type = value_type

    def __str__(self) -> str:
        return f"Param {{ subject: {self.subject}, value_type: {self.value_type} }}"


class ParsedType:
    def __init__(self) -> None:
        pass

    def type_type(self) -> ParsedTypeTypes:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()


class ParsedIdType(ParsedType):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def type_type(self) -> ParsedTypeTypes:
        return ParsedTypeTypes.Id

    def __str__(self) -> str:
        return f'IdType {{ value: "{self.value}" }}'


class ParsedExprTypes(Enum):
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


class ParsedExpr:
    def __init__(self) -> None:
        pass

    def expr_type(self) -> ParsedExprTypes:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()


class ParsedId(ParsedExpr):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ParsedExprTypes:
        return ParsedExprTypes.Id

    def __str__(self) -> str:
        return f'Id {{ value: "{self.value}" }}'


class ParsedInt(ParsedExpr):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ParsedExprTypes:
        return ParsedExprTypes.Int

    def __str__(self) -> str:
        return f"Int {{ value: {self.value} }}"


class ParsedFloat(ParsedExpr):
    def __init__(self, value: float) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ParsedExprTypes:
        return ParsedExprTypes.Float

    def __str__(self) -> str:
        return f"Float {{ value: {self.value} }}"


class ParsedChar(ParsedExpr):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ParsedExprTypes:
        return ParsedExprTypes.Char

    def __str__(self) -> str:
        return f"Char {{ value: '{self.value}' }}"


class ParsedString(ParsedExpr):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ParsedExprTypes:
        return ParsedExprTypes.String

    def __str__(self) -> str:
        return f'String {{ value: "{self.value}" }}'


class ParsedBool(ParsedExpr):
    def __init__(self, value: bool) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ParsedExprTypes:
        return ParsedExprTypes.Bool

    def __str__(self) -> str:
        return f"Bool {{ value: {'true' if self.value else 'false'} }}"


class ParsedArray(ParsedExpr):
    def __init__(self, values: List[ParsedExpr]) -> None:
        super().__init__()
        self.values = values

    def expr_type(self) -> ParsedExprTypes:
        return ParsedExprTypes.Array

    def __str__(self) -> str:
        values = ", ".join(str(value) for value in self.values)
        return f"Array {{ values: [ {values} ] }}"


class ParsedObject(ParsedExpr):
    def __init__(self, values: List[Tuple[str, ParsedExpr]]) -> None:
        super().__init__()
        self.values = values

    def expr_type(self) -> ParsedExprTypes:
        return ParsedExprTypes.Object

    def __str__(self) -> str:
        values = ", ".join(
            str(f'{{ key: "{key}", value: {value} }}') for (key, value) in self.values
        )
        return f"Object {{ values: [ {values} ] }}"


class ParsedAccessing(ParsedExpr):
    def __init__(self, subject: ParsedExpr, value: str) -> None:
        super().__init__()
        self.subject = subject
        self.value = value

    def expr_type(self) -> ParsedExprTypes:
        return ParsedExprTypes.Accessing

    def __str__(self) -> str:
        return f"Accessing {{ subject: {self.subject}, value: {self.value} }}"


class ParsedIndexing(ParsedExpr):
    def __init__(self, subject: ParsedExpr, value: ParsedExpr) -> None:
        super().__init__()
        self.subject = subject
        self.value = value

    def expr_type(self) -> ParsedExprTypes:
        return ParsedExprTypes.Indexing

    def __str__(self) -> str:
        return f"Indexing {{ subject: {self.subject}, value: {self.value} }}"


class ParsedCall(ParsedExpr):
    def __init__(self, subject: ParsedExpr, args: List[ParsedExpr]) -> None:
        super().__init__()
        self.subject = subject
        self.args = args

    def expr_type(self) -> ParsedExprTypes:
        return ParsedExprTypes.Call

    def __str__(self) -> str:
        args = ", ".join(str(arg) for arg in self.args)
        return f"Call {{ subject: {self.subject}, args: [ {args} ] }}"


class ParsedUnaryOperations(Enum):
    Not = auto()


class ParsedUnary(ParsedExpr):
    def __init__(self, subject: ParsedExpr, operation: ParsedUnaryOperations) -> None:
        super().__init__()
        self.subject = subject
        self.operation = operation

    def expr_type(self) -> ParsedExprTypes:
        return ParsedExprTypes.Unary

    def __str__(self) -> str:
        return f"Unary {{ subject: {self.subject}, operation: {self.operation} }}"


class ParsedBinaryOperations(Enum):
    Add = auto()
    Subtract = auto()
    Multiply = auto()
    EQ = auto()
    NE = auto()
    LT = auto()
    LTE = auto()
    GT = auto()
    GTE = auto()


class ParsedBinary(ParsedExpr):
    def __init__(
        self, left: ParsedExpr, right: ParsedExpr, operation: ParsedBinaryOperations
    ) -> None:
        super().__init__()
        self.left = left
        self.right = right
        self.operation = operation

    def expr_type(self) -> ParsedExprTypes:
        return ParsedExprTypes.Binary

    def __str__(self) -> str:
        return f"Binary {{ left: {self.left}, right: {self.right}, operation: {self.operation} }}"


class ParsedAssignOperations(Enum):
    Assign = auto()
    Increment = auto()
    Decrement = auto()


class ParsedAssign(ParsedExpr):
    def __init__(
        self, subject: ParsedExpr, value: ParsedExpr, operation: ParsedAssignOperations
    ) -> None:
        super().__init__()
        self.subject = subject
        self.value = value
        self.operation = operation

    def expr_type(self) -> ParsedExprTypes:
        return ParsedExprTypes.Assign

    def __str__(self) -> str:
        return f"Unary {{ subject: {self.subject}, value: {self.value}, operation: {self.operation} }}"


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.index = 0

    def done(self) -> bool:
        return self.index >= len(self.tokens)

    def step(self) -> None:
        self.index += 1

    def current(self) -> Token:
        return self.tokens[self.index]

    def current_type(self) -> TokenTypes:
        return self.tokens[self.index].tt

    def stepAndReturn(self, value: Any) -> Any:
        self.step()
        return value

    def expect(self, tt: TokenTypes) -> None:
        if self.current_type() != tt:
            raise Exception(f"expected '{tt}', got {self.current()}")

    def parse_statements(self) -> List[ParsedStatement]:
        statements: List[ParsedStatement] = []
        while not self.done() and self.current_type() == TokenTypes.Semicolon:
            self.step()
        while not self.done() and self.current_type() not in [
            TokenTypes.KwSlut,
            TokenTypes.KwEllers,
        ]:
            statements.append(self.parse_statement())
            while not self.done() and self.current_type() == TokenTypes.Semicolon:
                self.step()
        return statements

    def parse_statement(self) -> ParsedStatement:
        if self.done():
            return self.parse_expr_statement()
        elif self.current_type() == TokenTypes.KwFunktion:
            return self.parse_func()
        elif self.current_type() == TokenTypes.KwTilbagesend:
            return self.parse_return()
        elif self.current_type() == TokenTypes.KwMens:
            return self.parse_while()
        elif self.current_type() == TokenTypes.KwBryd:
            return self.parse_break()
        elif self.current_type() == TokenTypes.KwHvis:
            return self.parse_if()
        elif self.current_type() == TokenTypes.KwLad:
            return self.parse_let()
        else:
            return self.parse_expr_statement()

    def parse_func(self) -> ParsedFunc:
        self.step()
        self.expect(TokenTypes.Id)
        subject = self.current().value
        self.step()
        self.expect(TokenTypes.LParen)
        self.step()
        params: List[ParsedParam] = []
        while not self.done() and self.current_type() != TokenTypes.RParen:
            self.expect(TokenTypes.Id)
            value = self.current().value
            self.step()
            self.expect(TokenTypes.Colon)
            self.step()
            value_type = self.parse_type()
            params.append(ParsedParam(value, value_type))
            if self.current_type() == TokenTypes.Comma:
                self.step()
            else:
                break
        self.expect(TokenTypes.RParen)
        self.step()
        self.expect(TokenTypes.ThinArrow)
        self.step()
        return_type = self.parse_type()
        body = self.parse_statements()
        self.expect(TokenTypes.KwSlut)
        self.step()
        return ParsedFunc(subject, params, return_type, body)

    def parse_return(self) -> ParsedReturn:
        self.step()
        if not self.done() and self.current_type() in [
            TokenTypes.Semicolon,
            TokenTypes.KwFunktion,
            TokenTypes.KwTilbagesend,
            TokenTypes.KwMens,
            TokenTypes.KwBryd,
            TokenTypes.KwHvis,
            TokenTypes.KwLad,
            TokenTypes.KwSlut,
        ]:
            return ParsedReturn(None)
        else:
            return ParsedReturn(self.parse_expr())

    def parse_while(self) -> ParsedWhile:
        self.step()
        condition = self.parse_expr()
        self.expect(TokenTypes.KwSå)
        self.step()
        body = self.parse_statements()
        self.expect(TokenTypes.KwSlut)
        self.step()
        return ParsedWhile(condition, body)

    def parse_break(self) -> ParsedBreak:
        self.step()
        return ParsedBreak()

    def parse_if(self) -> ParsedIf:
        self.step()
        condition = self.parse_expr()
        self.expect(TokenTypes.KwSå)
        self.step()
        truthy = self.parse_statements()
        if self.current_type() == TokenTypes.KwSlut:
            self.step()
            return ParsedIf(condition, truthy, [])
        elif self.current_type() == TokenTypes.KwEllers:
            self.step()
            if self.current_type() == TokenTypes.KwHvis:
                elsecase = self.parse_if()
                return ParsedIf(condition, truthy, [elsecase])
            else:
                falsy = self.parse_statements()
                self.expect(TokenTypes.KwSlut)
                self.step()
                return ParsedIf(condition, truthy, falsy)
        else:
            raise Exception(f"expected 'ellers' or 'slut', got {self.current()}")

    def parse_let(self) -> ParsedLet:
        self.step()
        self.expect(TokenTypes.Id)
        subject = self.current().value
        self.step()
        self.expect(TokenTypes.Colon)
        self.step()
        value_type = self.parse_type()
        self.expect(TokenTypes.Assign)
        self.step()
        value = self.parse_expr()
        return ParsedLet(subject, value_type, value)

    def parse_expr_statement(self) -> ParsedExprStatement:
        return ParsedExprStatement(self.parse_expr())

    def parse_type(self) -> ParsedType:
        if self.current_type() == TokenTypes.Id:
            value = self.current().value
            self.step()
            return ParsedIdType(value)
        else:
            raise Exception(f"expected type, got {self.current()}")

    def parse_expr(self) -> ParsedExpr:
        if self.current_type() == TokenTypes.LBrace:
            return self.parse_object()
        elif self.current_type() == TokenTypes.LBracket:
            return self.parse_array()
        else:
            return self.parse_assignment()

    def parse_object(self) -> ParsedObject:
        self.step()
        values: List[Tuple[str, ParsedExpr]] = []
        while not self.done() and self.current_type() != TokenTypes.RBrace:
            self.expect(TokenTypes.Id)
            key = self.current().value
            self.step()
            self.expect(TokenTypes.Colon)
            self.step()
            value = self.parse_expr()
            if self.current_type() == TokenTypes.Comma:
                self.step()
            else:
                break
        self.expect(TokenTypes.RBrace)
        self.step()
        return ParsedObject(values)

    def parse_array(self) -> ParsedArray:
        self.step()
        values: List[ParsedExpr] = []
        while not self.done() and self.current_type() != TokenTypes.RBracket:
            values.append(self.parse_expr())
            if self.current_type() == TokenTypes.Comma:
                self.step()
            else:
                break
        self.expect(TokenTypes.RBracket)
        self.step()
        return ParsedArray(values)

    def parse_assignment(self) -> ParsedExpr:
        subject = self.parse_binary()
        if self.done():
            return subject
        elif self.current_type() == TokenTypes.Assign:
            self.step()
            return ParsedAssign(
                subject, self.parse_assignment(), ParsedAssignOperations.Assign
            )
        elif self.current_type() == TokenTypes.PlusAssign:
            self.step()
            return ParsedAssign(
                subject, self.parse_assignment(), ParsedAssignOperations.Increment
            )
        elif self.current_type() == TokenTypes.MinusAssign:
            self.step()
            return ParsedAssign(
                subject, self.parse_assignment(), ParsedAssignOperations.Decrement
            )
        else:
            return subject

    def parse_binary(self) -> ParsedExpr:
        expr_stack: List[ParsedExpr] = []
        op_stack: List[ParsedBinaryOperations] = []
        expr_stack.append(self.parse_unary())
        last_prec = 5
        while not self.done():
            op = self.maybe_parse_binary_op()
            if not op:
                break
            prec = self.binary_op_precedence(op)
            right = self.parse_unary()
            while prec <= last_prec and len(expr_stack) > 1:
                right_ = expr_stack.pop()
                op_ = op_stack.pop()
                last_prec = self.binary_op_precedence(op_)
                if last_prec < prec:
                    expr_stack.append(right_)
                    op_stack.append(op_)
                    break
                left = expr_stack.pop()
                expr_stack.append(ParsedBinary(left, right_, op_))
            expr_stack.append(right)
            op_stack.append(op)
        while len(expr_stack) > 1:
            right = expr_stack.pop()
            left = expr_stack.pop()
            op = op_stack.pop()
            expr_stack.append(ParsedBinary(left, right, op))
        return expr_stack[0]

    def maybe_parse_binary_op(self) -> Optional[ParsedBinaryOperations]:
        if self.current_type() == TokenTypes.Plus:
            return self.stepAndReturn(ParsedBinaryOperations.Add)
        elif self.current_type() == TokenTypes.Minus:
            return self.stepAndReturn(ParsedBinaryOperations.Subtract)
        elif self.current_type() == TokenTypes.Asterisk:
            return self.stepAndReturn(ParsedBinaryOperations.Multiply)
        elif self.current_type() == TokenTypes.EQ:
            return self.stepAndReturn(ParsedBinaryOperations.EQ)
        elif self.current_type() == TokenTypes.NE:
            return self.stepAndReturn(ParsedBinaryOperations.NE)
        elif self.current_type() == TokenTypes.LT:
            return self.stepAndReturn(ParsedBinaryOperations.LT)
        elif self.current_type() == TokenTypes.LTE:
            return self.stepAndReturn(ParsedBinaryOperations.LTE)
        elif self.current_type() == TokenTypes.GT:
            return self.stepAndReturn(ParsedBinaryOperations.GT)
        elif self.current_type() == TokenTypes.GTE:
            return self.stepAndReturn(ParsedBinaryOperations.GTE)
        else:
            return None

    def binary_op_precedence(self, op: ParsedBinaryOperations) -> int:
        if op == ParsedBinaryOperations.Add:
            return 3
        elif op == ParsedBinaryOperations.Subtract:
            return 3
        elif op == ParsedBinaryOperations.Multiply:
            return 4
        elif op == ParsedBinaryOperations.EQ:
            return 1
        elif op == ParsedBinaryOperations.NE:
            return 1
        elif op == ParsedBinaryOperations.LT:
            return 2
        elif op == ParsedBinaryOperations.LTE:
            return 2
        elif op == ParsedBinaryOperations.GT:
            return 2
        elif op == ParsedBinaryOperations.GTE:
            return 2
        else:
            raise Exception(f"unexhaustive match, got {op}")

    def parse_unary(self) -> ParsedExpr:
        if not self.done() and self.current_type() == TokenTypes.KwIkke:
            self.step()
            return ParsedUnary(self.parse_unary(), ParsedUnaryOperations.Not)
        else:
            return self.parse_call()

    def parse_call(self) -> ParsedExpr:
        subject = self.parse_indexing()
        if not self.done() and self.current_type() == TokenTypes.LParen:
            self.step()
            args: List[ParsedExpr] = []
            if self.current_type() not in [TokenTypes.RParen, TokenTypes.Comma]:
                args.append(self.parse_expr())
                while self.current_type() == TokenTypes.Comma:
                    self.step()
                    if self.current_type() == TokenTypes.RParen:
                        break
                    args.append(self.parse_expr())
            self.expect(TokenTypes.RParen)
            self.step()
            return ParsedCall(subject, args)
        else:
            return subject

    def parse_indexing(self) -> ParsedExpr:
        subject = self.parse_accessing()
        if not self.done() and self.current_type() == TokenTypes.LBracket:
            self.step()
            value = self.parse_expr()
            self.expect(TokenTypes.RBracket)
            self.step()
            return ParsedIndexing(subject, value)
        else:
            return subject

    def parse_accessing(self) -> ParsedExpr:
        subject = self.parse_group()
        if not self.done() and self.current_type() == TokenTypes.Dot:
            self.step()
            self.expect(TokenTypes.Id)
            value = self.current().value
            self.step()
            return ParsedAccessing(subject, value)
        else:
            return subject

    def parse_group(self) -> ParsedExpr:
        if not self.done() and self.current_type() == TokenTypes.LParen:
            self.step()
            expr = self.parse_expr()
            self.expect(TokenTypes.RParen)
            self.step()
            return expr
        return self.parse_value()

    def parse_value(self) -> ParsedExpr:
        if self.done():
            raise Exception(f"expected value")
        elif self.current_type() == TokenTypes.Id:
            return self.stepAndReturn(ParsedId(self.current().value))
        elif self.current_type() == TokenTypes.Int:
            return self.stepAndReturn(ParsedInt(int(self.current().value)))
        elif self.current_type() == TokenTypes.Float:
            return self.stepAndReturn(ParsedFloat(float(self.current().value)))
        elif self.current_type() == TokenTypes.Char:
            return self.stepAndReturn(ParsedChar(self.current().value))
        elif self.current_type() == TokenTypes.String:
            return self.stepAndReturn(ParsedString(self.current().value))
        elif self.current_type() == TokenTypes.KwFalsk:
            return self.stepAndReturn(ParsedBool(False))
        elif self.current_type() == TokenTypes.KwSand:
            return self.stepAndReturn(ParsedBool(True))
        else:
            raise Exception(f"expected value, got {self.current()}")
