from __future__ import annotations
from enum import Enum, auto
from typing import Any, List, Optional, Tuple
from tokenizer import Token, TokenTypes


class StatementType(Enum):
    Expr = auto()
    Let = auto()
    If = auto()
    While = auto()
    Break = auto()
    Func = auto()
    Return = auto()


class Statement:
    def __init__(self) -> None:
        pass

    def statement_type(self) -> StatementType:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()


def statements_to_string(statements: List[Statement]) -> str:
    statements_ = "\n".join(str(statement) for statement in statements)
    return f"[ {statements_} ]"


class ExprStatement(Statement):
    def __init__(self, value: Expr) -> None:
        super().__init__()
        self.value = value

    def statement_type(self) -> StatementType:
        return StatementType.Expr

    def __str__(self) -> str:
        return f"ExprStatement {{ value: {self.value} }}"


class Let(Statement):
    def __init__(self, subject: str, value: Expr) -> None:
        super().__init__()
        self.subject = subject
        self.value = value

    def statement_type(self) -> StatementType:
        return StatementType.Let

    def __str__(self) -> str:
        return f"Let {{ subject: {self.subject}, value: {self.value} }}"


class If(Statement):
    def __init__(
        self, condition: Expr, truthy: List[Statement], falsy: List[Statement]
    ) -> None:
        super().__init__()
        self.condition = condition
        self.truthy = truthy
        self.falsy = falsy

    def statement_type(self) -> StatementType:
        return StatementType.If

    def __str__(self) -> str:
        truthy = ", ".join(str(statement) for statement in self.truthy)
        falsy = ", ".join(str(statement) for statement in self.falsy)
        return f"If {{ condition: {self.condition}, truthy: [ {truthy} ], falsy: [ {falsy} ] }}"


class While(Statement):
    def __init__(self, condition: Expr, body: List[Statement]) -> None:
        super().__init__()
        self.condition = condition
        self.body = body

    def statement_type(self) -> StatementType:
        return StatementType.While

    def __str__(self) -> str:
        body = ", ".join(str(statement) for statement in self.body)
        return f"If {{ condition: {self.condition}, body: [ {body} ] }}"


class Break(Statement):
    def __init__(self) -> None:
        super().__init__()

    def statement_type(self) -> StatementType:
        return StatementType.While

    def __str__(self) -> str:
        return f"Break"


class Func(Statement):
    def __init__(self, subject: str, args: List[str], body: List[Statement]) -> None:
        super().__init__()
        self.subject = subject
        self.args = args
        self.body = body

    def statement_type(self) -> StatementType:
        return StatementType.While

    def __str__(self) -> str:
        args = ", ".join(f'"{arg}"' for arg in self.args)
        body = ", ".join(str(statement) for statement in self.body)
        return f"Func {{ subject: {self.subject}, args: [ {args} ], body: [ {body} ] }}"


class Return(Statement):
    def __init__(self, value: Optional[Expr]) -> None:
        super().__init__()
        self.value = value

    def statement_type(self) -> StatementType:
        return StatementType.Expr

    def __str__(self) -> str:
        return f"Return {{ value: {self.value} }}"


class ExprType(Enum):
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


class Expr:
    def __init__(self) -> None:
        pass

    def expr_type(self) -> ExprType:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()


class Id(Expr):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ExprType:
        return ExprType.Id

    def __str__(self) -> str:
        return f'Id {{ value: "{self.value}" }}'


class Int(Expr):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ExprType:
        return ExprType.Int

    def __str__(self) -> str:
        return f"Int {{ value: {self.value} }}"


class Float(Expr):
    def __init__(self, value: float) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ExprType:
        return ExprType.Float

    def __str__(self) -> str:
        return f"Float {{ value: {self.value} }}"


class Char(Expr):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ExprType:
        return ExprType.Char

    def __str__(self) -> str:
        return f"Char {{ value: '{self.value}' }}"


class String(Expr):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ExprType:
        return ExprType.String

    def __str__(self) -> str:
        return f'String {{ value: "{self.value}" }}'


class Bool(Expr):
    def __init__(self, value: bool) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ExprType:
        return ExprType.Bool

    def __str__(self) -> str:
        return f"Bool {{ value: {'true' if self.value else 'false'} }}"


class Array(Expr):
    def __init__(self, values: List[Expr]) -> None:
        super().__init__()
        self.values = values

    def expr_type(self) -> ExprType:
        return ExprType.Array

    def __str__(self) -> str:
        values = ", ".join(str(value) for value in self.values)
        return f"Array {{ values: [ {values} ] }}"


class Object(Expr):
    def __init__(self, values: List[Tuple[str, Expr]]) -> None:
        super().__init__()
        self.values = values

    def expr_type(self) -> ExprType:
        return ExprType.Object

    def __str__(self) -> str:
        values = ", ".join(
            str(f'{{ key: "{key}", value: {value} }}') for (key, value) in self.values
        )
        return f"Object {{ values: [ {values} ] }}"


class Accessing(Expr):
    def __init__(self, subject: Expr, value: str) -> None:
        super().__init__()
        self.subject = subject
        self.value = value

    def expr_type(self) -> ExprType:
        return ExprType.Accessing

    def __str__(self) -> str:
        return f"Accessing {{ subject: {self.subject}, value: {self.value} }}"


class Indexing(Expr):
    def __init__(self, subject: Expr, value: Expr) -> None:
        super().__init__()
        self.subject = subject
        self.value = value

    def expr_type(self) -> ExprType:
        return ExprType.Indexing

    def __str__(self) -> str:
        return f"Indexing {{ subject: {self.subject}, value: {self.value} }}"


class Call(Expr):
    def __init__(self, subject: Expr, args: List[Expr]) -> None:
        super().__init__()
        self.subject = subject
        self.args = args

    def expr_type(self) -> ExprType:
        return ExprType.Call

    def __str__(self) -> str:
        args = ", ".join(str(arg) for arg in self.args)
        return f"Call {{ subject: {self.subject}, args: [ {args} ] }}"


class UnaryOperations(Enum):
    Not = auto()


class Unary(Expr):
    def __init__(self, subject: Expr, operation: UnaryOperations) -> None:
        super().__init__()
        self.subject = subject
        self.operation = operation

    def expr_type(self) -> ExprType:
        return ExprType.Unary

    def __str__(self) -> str:
        return f"Unary {{ subject: {self.subject}, operation: {self.operation} }}"


class BinaryOperations(Enum):
    Add = auto()
    Subtract = auto()
    Multiply = auto()
    EQ = auto()
    NE = auto()
    LT = auto()
    LTE = auto()
    GT = auto()
    GTE = auto()


class Binary(Expr):
    def __init__(self, left: Expr, right: Expr, operation: BinaryOperations) -> None:
        super().__init__()
        self.left = left
        self.right = right
        self.operation = operation

    def expr_type(self) -> ExprType:
        return ExprType.Binary

    def __str__(self) -> str:
        return f"Binary {{ left: {self.left}, right: {self.right}, operation: {self.operation} }}"


class AssignOperations(Enum):
    Assign = auto()
    Increment = auto()
    Decrement = auto()


class Assign(Expr):
    def __init__(self, subject: Expr, value: Expr, operation: AssignOperations) -> None:
        super().__init__()
        self.subject = subject
        self.value = value
        self.operation = operation

    def expr_type(self) -> ExprType:
        return ExprType.Assign

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

    def parse_statements(self) -> List[Statement]:
        statements: List[Statement] = []
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

    def parse_statement(self) -> Statement:
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

    def parse_func(self) -> Func:
        self.step()
        self.expect(TokenTypes.Id)
        subject = self.current().value
        self.step()
        self.expect(TokenTypes.LParen)
        self.step()
        args: List[str] = []
        while not self.done() and self.current_type() != TokenTypes.RParen:
            self.expect(TokenTypes.Id)
            args.append(self.current().value)
            self.step()
            if self.current_type() == TokenTypes.Comma:
                self.step()
            else:
                break
        self.expect(TokenTypes.RParen)
        self.step()
        body = self.parse_statements()
        self.expect(TokenTypes.KwSlut)
        self.step()
        return Func(subject, args, body)

    def parse_return(self) -> Return:
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
            return Return(None)
        else:
            return Return(self.parse_expr())

    def parse_while(self) -> While:
        self.step()
        condition = self.parse_expr()
        self.expect(TokenTypes.KwSå)
        self.step()
        body = self.parse_statements()
        self.expect(TokenTypes.KwSlut)
        self.step()
        return While(condition, body)

    def parse_break(self) -> Break:
        self.step()
        return Break()

    def parse_if(self) -> If:
        self.step()
        condition = self.parse_expr()
        self.expect(TokenTypes.KwSå)
        self.step()
        truthy = self.parse_statements()
        if self.current_type() == TokenTypes.KwSlut:
            self.step()
            return If(condition, truthy, [])
        elif self.current_type() == TokenTypes.KwEllers:
            self.step()
            if self.current_type() == TokenTypes.KwHvis:
                elsecase = self.parse_if()
                return If(condition, truthy, [elsecase])
            else:
                falsy = self.parse_statements()
                self.expect(TokenTypes.KwSlut)
                self.step()
                return If(condition, truthy, falsy)
        else:
            raise Exception(f"expected 'ellers' or 'slut', got {self.current()}")

    def parse_let(self) -> Let:
        self.step()
        self.expect(TokenTypes.Id)
        subject = self.current().value
        self.step()
        self.expect(TokenTypes.Assign)
        self.step()
        value = self.parse_expr()
        return Let(subject, value)

    def parse_expr_statement(self) -> ExprStatement:
        return ExprStatement(self.parse_expr())

    def parse_expr(self) -> Expr:
        if self.current_type() == TokenTypes.LBrace:
            return self.parse_object()
        elif self.current_type() == TokenTypes.LBracket:
            return self.parse_array()
        else:
            return self.parse_assignment()

    def parse_object(self) -> Object:
        self.step()
        values: List[Tuple[str, Expr]] = []
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
        return Object(values)

    def parse_array(self) -> Array:
        self.step()
        values: List[Expr] = []
        while not self.done() and self.current_type() != TokenTypes.RBracket:
            values.append(self.parse_expr())
            if self.current_type() == TokenTypes.Comma:
                self.step()
            else:
                break
        self.expect(TokenTypes.RBracket)
        self.step()
        return Array(values)

    def parse_assignment(self) -> Expr:
        subject = self.parse_binary()
        if self.done():
            return subject
        elif self.current_type() == TokenTypes.Assign:
            self.step()
            return Assign(subject, self.parse_assignment(), AssignOperations.Assign)
        elif self.current_type() == TokenTypes.PlusAssign:
            self.step()
            return Assign(subject, self.parse_assignment(), AssignOperations.Increment)
        elif self.current_type() == TokenTypes.MinusAssign:
            self.step()
            return Assign(subject, self.parse_assignment(), AssignOperations.Decrement)
        else:
            return subject

    def parse_binary(self) -> Expr:
        expr_stack: List[Expr] = []
        op_stack: List[BinaryOperations] = []
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
                expr_stack.append(Binary(left, right_, op_))
            expr_stack.append(right)
            op_stack.append(op)
        while len(expr_stack) > 1:
            right = expr_stack.pop()
            left = expr_stack.pop()
            op = op_stack.pop()
            expr_stack.append(Binary(left, right, op))
        return expr_stack[0]

    def maybe_parse_binary_op(self) -> Optional[BinaryOperations]:
        if self.current_type() == TokenTypes.Plus:
            return self.stepAndReturn(BinaryOperations.Add)
        elif self.current_type() == TokenTypes.Minus:
            return self.stepAndReturn(BinaryOperations.Subtract)
        elif self.current_type() == TokenTypes.Asterisk:
            return self.stepAndReturn(BinaryOperations.Multiply)
        elif self.current_type() == TokenTypes.EQ:
            return self.stepAndReturn(BinaryOperations.EQ)
        elif self.current_type() == TokenTypes.NE:
            return self.stepAndReturn(BinaryOperations.NE)
        elif self.current_type() == TokenTypes.LT:
            return self.stepAndReturn(BinaryOperations.LT)
        elif self.current_type() == TokenTypes.LTE:
            return self.stepAndReturn(BinaryOperations.LTE)
        elif self.current_type() == TokenTypes.GT:
            return self.stepAndReturn(BinaryOperations.GT)
        elif self.current_type() == TokenTypes.GTE:
            return self.stepAndReturn(BinaryOperations.GTE)
        else:
            return None

    def binary_op_precedence(self, op: BinaryOperations) -> int:
        if op == BinaryOperations.Add:
            return 3
        elif op == BinaryOperations.Subtract:
            return 3
        elif op == BinaryOperations.Multiply:
            return 4
        elif op == BinaryOperations.EQ:
            return 1
        elif op == BinaryOperations.NE:
            return 1
        elif op == BinaryOperations.LT:
            return 2
        elif op == BinaryOperations.LTE:
            return 2
        elif op == BinaryOperations.GT:
            return 2
        elif op == BinaryOperations.GTE:
            return 2
        else:
            raise Exception(f"unexhaustive match, got {op}")

    def parse_unary(self) -> Expr:
        if not self.done() and self.current_type() == TokenTypes.KwIkke:
            self.step()
            return Unary(self.parse_unary(), UnaryOperations.Not)
        else:
            return self.parse_call()

    def parse_call(self) -> Expr:
        subject = self.parse_indexing()
        if not self.done() and self.current_type() == TokenTypes.LParen:
            self.step()
            args: List[Expr] = []
            if self.current_type() not in [TokenTypes.RParen, TokenTypes.Comma]:
                args.append(self.parse_expr())
                while self.current_type() == TokenTypes.Comma:
                    self.step()
                    if self.current_type() == TokenTypes.RParen:
                        break
                    args.append(self.parse_expr())
            self.expect(TokenTypes.RParen)
            self.step()
            return Call(subject, args)
        else:
            return subject

    def parse_indexing(self) -> Expr:
        subject = self.parse_accessing()
        if not self.done() and self.current_type() == TokenTypes.LBracket:
            self.step()
            value = self.parse_expr()
            self.expect(TokenTypes.RBracket)
            self.step()
            return Indexing(subject, value)
        else:
            return subject

    def parse_accessing(self) -> Expr:
        subject = self.parse_group()
        if not self.done() and self.current_type() == TokenTypes.Dot:
            self.step()
            self.expect(TokenTypes.Id)
            value = self.current().value
            self.step()
            return Accessing(subject, value)
        else:
            return subject

    def parse_group(self) -> Expr:
        if not self.done() and self.current_type() == TokenTypes.LParen:
            self.step()
            expr = self.parse_expr()
            self.expect(TokenTypes.RParen)
            self.step()
            return expr
        return self.parse_value()

    def parse_value(self) -> Expr:
        if self.done():
            raise Exception(f"expected value")
        elif self.current_type() == TokenTypes.Id:
            return self.stepAndReturn(Id(self.current().value))
        elif self.current_type() == TokenTypes.Int:
            return self.stepAndReturn(Int(int(self.current().value)))
        elif self.current_type() == TokenTypes.Float:
            return self.stepAndReturn(Float(float(self.current().value)))
        elif self.current_type() == TokenTypes.Char:
            return self.stepAndReturn(Char(self.current().value))
        elif self.current_type() == TokenTypes.String:
            return self.stepAndReturn(String(self.current().value))
        elif self.current_type() == TokenTypes.KwFalsk:
            return self.stepAndReturn(Bool(False))
        elif self.current_type() == TokenTypes.KwSand:
            return self.stepAndReturn(Bool(True))
        else:
            raise Exception(f"expected value, got {self.current()}")
