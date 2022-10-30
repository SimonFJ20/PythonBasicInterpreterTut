from __future__ import annotations
from enum import Enum, auto
from typing import Any, List, Optional, Tuple

class TokenTypes(Enum):
    Id = auto()
    Int = auto()
    Float = auto()
    Char = auto()
    String = auto()
    KwIkke = auto()
    KwLad = auto()
    KwHvis = auto()
    KwSå = auto()
    KwEllers = auto()
    KwMens = auto()
    KwBryd = auto()
    KwSlut = auto()
    KwFunktion = auto()
    KwTilbagesend = auto()
    KwFalsk = auto()
    KwSand = auto()
    LParen = auto()
    RParen = auto()
    LBrace = auto()
    RBrace = auto()
    LBracket = auto()
    RBracket = auto()
    Dot = auto()
    Comma = auto()
    Colon = auto()
    Semicolon = auto()
    Plus = auto()
    Minus = auto()
    Asterisk = auto()
    Assign = auto()
    PlusAssign = auto()
    MinusAssign = auto()
    EQ = auto()
    NE = auto()
    LT = auto()
    LTE = auto()
    GT = auto()
    GTE = auto()

class Token:
    def __init__(self, tt: TokenTypes, value: str, line: int) -> None:
        self.tt = tt
        self.value = value
        self.line = line
    
    def __str__(self) -> str:
        return F"{{ tt: {self.tt}, value: \"{self.value}\", row: {self.line} }}"

def chars_match(pool: str, matcher: str) -> bool:
    if len(pool) < len(matcher):
        return False
    for i, v in enumerate(matcher):
        print(f"'{pool[i]}' == '{v}' == {pool[i] == v}, {ord(pool[i])} {ord(v)}")
        if pool[i] != v:
            return False
    return True

DIGITS = "1234567890"
ID_CHARS = "abcdefghijklmnopqrstuvwxyzæøåABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ_"

def tokenize(text: str) -> List[Token]:
    tokens: List[Token] = []
    i = 0
    line = 1
    while i < len(text):
        # print('"' + text[i:i+2] + '"', chars_match(text[i:], "så"), text[i:i+2] == "sǻ")
        if text[i] in " \t\r\n":
            if text[i] == "\n":
                line += 1
            i += 1
        elif chars_match(text[i:], "KOMMENTAR"):
            while i < len(text) and text[i] != '\n':
                i += 1
            i += 1
        elif chars_match(text[i:], "KOMMENTER"):
            while i < len(text) and not chars_match(text[i:], "FÆRDIG"):
                i += 1
            i += len("FÆRDIG")
        elif chars_match(text[i:], "ikke"):
            l = len("ikke")
            tokens.append(Token(TokenTypes.KwIkke, text[i : i + l], line))
            i += len("ikke")
        elif chars_match(text[i:], "lad"):
            l = len("lad")
            tokens.append(Token(TokenTypes.KwLad, text[i : i + l], line))
            i += l
        elif chars_match(text[i:], "hvis"):
            l = len("hvis")
            tokens.append(Token(TokenTypes.KwHvis, text[i : i + l], line))
            i += l
        elif chars_match(text[i:], "så"):
            l = len("så")
            tokens.append(Token(TokenTypes.KwSå, text[i : i + l], line))
            i += l
        elif chars_match(text[i:], "ellers"):
            l = len("ellers")
            tokens.append(Token(TokenTypes.KwEllers, text[i : i + l], line))
            i += l
        elif chars_match(text[i:], "mens"):
            l = len("mens")
            tokens.append(Token(TokenTypes.KwMens, text[i : i + l], line))
            i += l
        elif chars_match(text[i:], "bryd"):
            l = len("bryd")
            tokens.append(Token(TokenTypes.KwBryd, text[i : i + l], line))
            i += l
        elif chars_match(text[i:], "slut"):
            l = len("slut")
            tokens.append(Token(TokenTypes.KwSlut, text[i : i + l], line))
            i += l
        elif chars_match(text[i:], "funktion"):
            l = len("funktion")
            tokens.append(Token(TokenTypes.KwFunktion, text[i : i + l], line))
            i += l
        elif chars_match(text[i:], "tilbagesend"):
            l = len("tilbagesend")
            tokens.append(Token(TokenTypes.KwTilbagesend, text[i : i + l], line))
            i += l
        elif chars_match(text[i:], "falsk"):
            l = len("falsk")
            tokens.append(Token(TokenTypes.KwFalsk, text[i : i + l], line))
            i += l
        elif chars_match(text[i:], "sand"):
            l = len("sand")
            tokens.append(Token(TokenTypes.KwSand, text[i : i + l], line))
            i += l
        elif text[i] in ID_CHARS:
            value = text[i]
            i += 1
            while i < len(text) and text[i] in ID_CHARS + DIGITS:
                value += text[i]
                i += 1
            tokens.append(Token(TokenTypes.Id, value, line))
        elif text[i] in DIGITS:
            value = text[i]
            i += 1
            dots = 0
            while i < len(text) and text[i] in (DIGITS + "."):
                if text[i] == ".":
                    dots += 1
                value += text[i]
                i += 1
            if dots > 1:
                raise Exception("cannot have more than one decimal point")
            elif dots == 1:
                tokens.append(Token(TokenTypes.Float, value, line))
            else:
                tokens.append(Token(TokenTypes.Int, value, line))
        elif text[i] == "'":
            value = text[i]
            i += 1
            if i >= len(text): raise Exception("unfinished char literal")
            if text[i] == "\n": line += 1
            value += text[i]
            if text[i] == "\\":
                i += 1
                if i >= len(text): raise Exception("unfinished char literal")
                value += text[i]
            i += 1
            if i >= len(text) or text[i] != "'": raise Exception("unfinished char literal")
            value += text[i]
            i += 1
            tokens.append(Token(TokenTypes.Char, value, line))
        elif text[i] == "\"":
            value = text[i]
            i += 1
            escaped = False
            while i < len(text):
                if escaped:
                    escaped = False
                else:
                    if text[i] == "\"":
                        break
                    elif text[i] == "\\":
                        escaped = True
                if text[i] == "\n": line += 1
                value += text[i]
                i += 1
            if text[i] != "\"": raise Exception("unfinished string literal")
            value += text[i]
            i += 1
            tokens.append(Token(TokenTypes.String, value, line))
        elif chars_match(text[i:], "("):
            tokens.append(Token(TokenTypes.LParen, text[i], line))
            i += 1
        elif chars_match(text[i:], ")"):
            tokens.append(Token(TokenTypes.RParen, text[i], line))
            i += 1
        elif chars_match(text[i:], "{"):
            tokens.append(Token(TokenTypes.LBrace, text[i], line))
            i += 1
        elif chars_match(text[i:], "}"):
            tokens.append(Token(TokenTypes.RBrace, text[i], line))
            i += 1
        elif chars_match(text[i:], "["):
            tokens.append(Token(TokenTypes.LBracket, text[i], line))
            i += 1
        elif chars_match(text[i:], "]"):
            tokens.append(Token(TokenTypes.RBracket, text[i], line))
            i += 1
        elif chars_match(text[i:], "+="):
            tokens.append(Token(TokenTypes.PlusAssign, text[i : i + 2], line))
            i += 2
        elif chars_match(text[i:], "."):
            tokens.append(Token(TokenTypes.Dot, text[i], line))
            i += 1
        elif chars_match(text[i:], ","):
            tokens.append(Token(TokenTypes.Comma, text[i], line))
            i += 1
        elif chars_match(text[i:], ":"):
            tokens.append(Token(TokenTypes.Colon, text[i], line))
            i += 1
        elif chars_match(text[i:], ";"):
            tokens.append(Token(TokenTypes.Semicolon, text[i], line))
            i += 1
        elif chars_match(text[i:], "+"):
            tokens.append(Token(TokenTypes.Plus, text[i], line))
            i += 1
        elif chars_match(text[i:], "-"):
            tokens.append(Token(TokenTypes.Minus, text[i], line))
            i += 1
        elif chars_match(text[i:], "*"):
            tokens.append(Token(TokenTypes.Asterisk, text[i], line))
            i += 1
        elif chars_match(text[i:], "=="):
            tokens.append(Token(TokenTypes.EQ, text[i : i + 2], line))
            i += 2
        elif chars_match(text[i:], "!="):
            tokens.append(Token(TokenTypes.NE, text[i : i + 2], line))
            i += 2
        elif chars_match(text[i:], "<="):
            tokens.append(Token(TokenTypes.LTE, text[i : i + 2], line))
            i += 2
        elif chars_match(text[i:], "<"):
            tokens.append(Token(TokenTypes.LT, text[i], line))
            i += 1
        elif chars_match(text[i:], ">="):
            tokens.append(Token(TokenTypes.GTE, text[i : i + 2], line))
            i += 2
        elif chars_match(text[i:], ">"):
            tokens.append(Token(TokenTypes.GT, text[i], line))
            i += 1
        elif chars_match(text[i:], "="):
            tokens.append(Token(TokenTypes.Assign, text[i], line))
            i += 1
        else:
            raise Exception(f"invalid char '{text[i]}'")
    return tokens

def statements_to_string(statements: List[Statement]) -> str:
    statements_ = "\n".join(str(statement) for statement in statements)
    return f"[ {statements_} ]"

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

    def statement_type(self) -> StatementType: raise NotImplementedError()
    def __str__(self) -> str: raise NotImplementedError()

class ExprStatement(Statement):
    def __init__(self, value: Expr) -> None:
        super().__init__()
        self.value = value
    
    def statement_type(self) -> StatementType: return StatementType.Expr
    def __str__(self) -> str: return f"ExprStatement {{ value: {self.value} }}"

class Let(Statement):
    def __init__(self, subject: str, value: Expr) -> None:
        super().__init__()
        self.subject = subject
        self.value = value

    def statement_type(self) -> StatementType: return StatementType.Let
    def __str__(self) -> str: return f"Let {{ subject: {self.subject}, value: {self.value} }}"

class If(Statement):
    def __init__(self, condition: Expr, truthy: List[Statement], falsy: List[Statement]) -> None:
        super().__init__()
        self.condition = condition
        self.truthy = truthy
        self.falsy = falsy

    def statement_type(self) -> StatementType: return StatementType.If
    def __str__(self) -> str:
        truthy = ", ".join(str(statement) for statement in self.truthy)
        falsy = ", ".join(str(statement) for statement in self.falsy)
        return f"If {{ condition: {self.condition}, truthy: [ {truthy} ], falsy: [ {falsy} ] }}"

class While(Statement):
    def __init__(self, condition: Expr, body: List[Statement]) -> None:
        super().__init__()
        self.condition = condition
        self.body = body

    def statement_type(self) -> StatementType: return StatementType.While
    def __str__(self) -> str:
        body = ", ".join(str(statement) for statement in self.body)
        return f"If {{ condition: {self.condition}, body: [ {body} ] }}"

class Break(Statement):
    def __init__(self) -> None:
        super().__init__()

    def statement_type(self) -> StatementType: return StatementType.While
    def __str__(self) -> str:
        return f"Break"

class Func(Statement):
    def __init__(self, subject: str, args: List[str], body: List[Statement]) -> None:
        super().__init__()
        self.subject = subject
        self.args = args
        self.body = body

    def statement_type(self) -> StatementType: return StatementType.While
    def __str__(self) -> str:
        args = ", ".join(f"\"{arg}\"" for arg in self.args)
        body = ", ".join(str(statement) for statement in self.body)
        return f"Func {{ subject: {self.subject}, args: [ {args} ], body: [ {body} ] }}"

class Return(Statement):
    def __init__(self, value: Optional[Expr]) -> None:
        super().__init__()
        self.value = value
    
    def statement_type(self) -> StatementType: return StatementType.Expr
    def __str__(self) -> str: return f"Return {{ value: {self.value} }}"

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

    def expr_type(self) -> ExprType: raise NotImplementedError()
    def __str__(self) -> str: raise NotImplementedError()

class Id(Expr):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ExprType: return ExprType.Id
    def __str__(self) -> str: return f"Id {{ value: \"{self.value}\" }}"

class Int(Expr):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ExprType: return ExprType.Int
    def __str__(self) -> str: return f"Int {{ value: {self.value} }}"

class Float(Expr):
    def __init__(self, value: float) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ExprType: return ExprType.Float
    def __str__(self) -> str: return f"Float {{ value: {self.value} }}"

class Char(Expr):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ExprType: return ExprType.Char
    def __str__(self) -> str: return f"Char {{ value: \'{self.value}\' }}"

class String(Expr):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ExprType: return ExprType.String
    def __str__(self) -> str: return f"String {{ value: \"{self.value}\" }}"

class Bool(Expr):
    def __init__(self, value: bool) -> None:
        super().__init__()
        self.value = value

    def expr_type(self) -> ExprType: return ExprType.Bool
    def __str__(self) -> str:
        return f"Bool {{ value: {'true' if self.value else 'false'} }}"

class Array(Expr):
    def __init__(self, values: List[Expr]) -> None:
        super().__init__()
        self.values = values

    def expr_type(self) -> ExprType: return ExprType.Array
    def __str__(self) -> str:
        values = ", ".join(str(value) for value in self.values)
        return f"Array {{ values: [ {values} ] }}"

class Object(Expr):
    def __init__(self, values: List[Tuple[str, Expr]]) -> None:
        super().__init__()
        self.values = values

    def expr_type(self) -> ExprType: return ExprType.Object
    def __str__(self) -> str:
        values = ", ".join(str(f"{{ key: \"{key}\", value: {value} }}") for (key,value) in self.values)
        return f"Object {{ values: [ {values} ] }}"

class Accessing(Expr):
    def __init__(self, subject: Expr, value: str) -> None:
        super().__init__()
        self.subject = subject
        self.value = value

    def expr_type(self) -> ExprType: return ExprType.Accessing
    def __str__(self) -> str:
        return f"Accessing {{ subject: {self.subject}, value: {self.value} }}"

class Indexing(Expr):
    def __init__(self, subject: Expr, value: Expr) -> None:
        super().__init__()
        self.subject = subject
        self.value = value

    def expr_type(self) -> ExprType: return ExprType.Indexing
    def __str__(self) -> str:
        return f"Indexing {{ subject: {self.subject}, value: {self.value} }}"

class Call(Expr):
    def __init__(self, subject: Expr, args: List[Expr]) -> None:
        super().__init__()
        self.subject = subject
        self.args = args

    def expr_type(self) -> ExprType: return ExprType.Call
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

    def expr_type(self) -> ExprType: return ExprType.Unary
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

    def expr_type(self) -> ExprType: return ExprType.Binary
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

    def expr_type(self) -> ExprType: return ExprType.Assign
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
        while not self.done() and self.current_type() not in [TokenTypes.KwSlut, TokenTypes.KwEllers]:
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
            if not op: break
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
        if self.current_type() == TokenTypes.Plus: return self.stepAndReturn(BinaryOperations.Add)
        elif self.current_type() == TokenTypes.Minus: return self.stepAndReturn(BinaryOperations.Subtract)
        elif self.current_type() == TokenTypes.Asterisk: return self.stepAndReturn(BinaryOperations.Multiply)
        elif self.current_type() == TokenTypes.EQ: return self.stepAndReturn(BinaryOperations.EQ)
        elif self.current_type() == TokenTypes.NE: return self.stepAndReturn(BinaryOperations.NE)
        elif self.current_type() == TokenTypes.LT: return self.stepAndReturn(BinaryOperations.LT)
        elif self.current_type() == TokenTypes.LTE: return self.stepAndReturn(BinaryOperations.LTE)
        elif self.current_type() == TokenTypes.GT: return self.stepAndReturn(BinaryOperations.GT)
        elif self.current_type() == TokenTypes.GTE: return self.stepAndReturn(BinaryOperations.GTE)
        else: return None

    def binary_op_precedence(self, op: BinaryOperations) -> int:
        if op == BinaryOperations.Add: return 3
        elif op == BinaryOperations.Subtract: return 3
        elif op == BinaryOperations.Multiply: return 4
        elif op == BinaryOperations.EQ: return 1
        elif op == BinaryOperations.NE: return 1
        elif op == BinaryOperations.LT: return 2
        elif op == BinaryOperations.LTE: return 2
        elif op == BinaryOperations.GT: return 2
        elif op == BinaryOperations.GTE: return 2
        else: raise Exception(f"unexhaustive match, got {op}")

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


def main() -> None:
    with open("test.dk") as file:
        text = file.read()
        tokens = tokenize(text)
        parser = Parser(tokens)
        print("=== TOKEN ===")
        for token in tokens:
            print(token)
        ast = parser.parse_statements()
        print("=== AST ===")
        print(statements_to_string(ast))

if __name__ == "__main__":
    main()
