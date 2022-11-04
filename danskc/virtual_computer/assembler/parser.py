from enum import Enum, auto
from typing import List, Optional

class TokenType(Enum):
    EOF = auto()
    Name = auto()
    Int = auto()
    Hex = auto()
    DoubleAsterisk = auto()
    Plus = auto()
    Minus = auto()
    Asterisk = auto()
    Slash = auto()
    Percent = auto()
    Exclamation = auto()
    Ampersand = auto()
    Hat = auto()
    Pipe = auto()
    DoubleLT = auto()
    DoubleGT = auto()
    LParen = auto()
    RParen = auto()
    LBracket = auto()
    RBracket = auto()
    Comma = auto()
    Colon = auto()

class Token:
    def __init__(self, type: TokenType, value: str) -> None:
        self.type = type
        self.value = value
    
    def __str__(self) -> str:
        return f"({self.type}, \"{self.value}\")"

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "1234567890"
HEX_DIGITS = DIGITS + "abcdefABCDEF"

def tokenize(line: str) -> List[Token]:
    tokens: List[Token] = []
    i = 0
    while i < len(line):
        if line[i] in " \t\r\n":
            i += 1
        elif line[i] == ";":
            i = len(line)
        elif line[i] in LETTERS + "_.":
            value = line[i]
            i += 1
            while i < len(line) and line[i] in LETTERS + DIGITS + "_":
                value += line[i]
                i += 1
            tokens.append(Token(TokenType.Name, value))
        elif line[i] in "123456789":
            value = line[i]
            i += 1
            while i < len(line) and line[i] in DIGITS:
                value += line[i]
                i += 1
            tokens.append(Token(TokenType.Int, value))
        elif line[i] == "0":
            value = line[i]
            i += 1
            if i < len(line) and line[i] in "xX":
                i += 1
                while line[i] in HEX_DIGITS:
                    value += line[i]
                    i += 1
                tokens.append(Token(TokenType.Hex, value))
            else:
                tokens.append(Token(TokenType.Int, value))
        elif line[i] == "*":
            i += 1
            if line[i] == "*":
                i += 1
                tokens.append(Token(TokenType.DoubleAsterisk, "**"))
            else:
                tokens.append(Token(TokenType.Asterisk, "*"))
        elif line[i] == "+":
            i += 1
            tokens.append(Token(TokenType.Plus, "+"))
        elif line[i] == "-":
            i += 1
            tokens.append(Token(TokenType.Minus, "-"))
        elif line[i] == "/":
            i += 1
            tokens.append(Token(TokenType.Slash, "/"))
        elif line[i] == "%":
            i += 1
            tokens.append(Token(TokenType.Percent, "%"))
        elif line[i] == "!":
            i += 1
            tokens.append(Token(TokenType.Exclamation, "!"))
        elif line[i] == "&":
            i += 1
            tokens.append(Token(TokenType.Ampersand, "&"))
        elif line[i] == "|":
            i += 1
            tokens.append(Token(TokenType.Pipe, "|"))
        elif line[i] == "<":
            i += 1
            if line[i] == "<":
                i += 1
                tokens.append(Token(TokenType.DoubleLT, "<<"))
            else:
                raise Exception("\'<\' (less than) not implemented")
        elif line[i] == ">":
            i += 1
            if line[i] == ">":
                i += 1
                tokens.append(Token(TokenType.DoubleGT, ">>"))
            else:
                raise Exception("\'>\' (greater than) not implemented")
        elif line[i] == "(":
            i += 1
            tokens.append(Token(TokenType.LParen, "("))
        elif line[i] == ")":
            i += 1
            tokens.append(Token(TokenType.RParen, ")"))
        elif line[i] == "[":
            i += 1
            tokens.append(Token(TokenType.LBracket, "["))
        elif line[i] == "]":
            i += 1
            tokens.append(Token(TokenType.RBracket, "]"))
        elif line[i] == ",":
            i += 1
            tokens.append(Token(TokenType.Comma, ","))
        elif line[i] == ":":
            i += 1
            tokens.append(Token(TokenType.Colon, ":"))
        else:
            raise Exception(f"unexpected char \'{line[i]}\'")
    tokens.append(Token(TokenType.EOF, ""))
    return tokens

class AtomType(Enum):
    Name = auto()
    Int = auto()
    Hex = auto()

class Atom:
    def __init__(self) -> None:
        self.atom_type: AtomType

    def __str__(self) -> str:
        raise NotImplementedError()

    def to_json(self) -> str:
        raise NotImplementedError()

class Name(Atom):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.atom_type = AtomType.Name
        self.value = value

    def __str__(self) -> str:
        return f"{self.value}"

    def to_json(self) -> str:
        return f'''{{
            "type": "atom",
            "atomType": "name",
            "value": "{self.value}"
        }}'''

class Int(Atom):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.atom_type = AtomType.Int
        self.value = int(value)

    def __str__(self) -> str:
        return f"{self.value}"

    def to_json(self) -> str:
        return f'''{{
            "type": "atom",
            "atomType": "int",
            "value": {self.value}
        }}'''

class Hex(Atom):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.atom_type = AtomType.Hex
        self.value = int(value, 16)

    def __str__(self) -> str:
        return f"{self.value}"

    def to_json(self) -> str:
        return f'''{{
            "type": "atom",
            "atomType": "int",
            "value": 0x{self.value}
        }}'''

class ExprType(Enum):
    Binary = auto()
    Not = auto()
    Atom = auto()

class Expr:
    def __init__(self) -> None:
        self.expr_type: ExprType

    def __str__(self) -> str:
        raise NotImplementedError()

    def to_json(self) -> str:
        raise NotImplementedError()

class BinaryType(Enum):
    Add = auto()
    Subtract = auto()
    Multiply = auto()
    Divide = auto()
    Modolus = auto()
    Power = auto()
    And = auto()
    Or = auto()
    Xor = auto()
    ShiftLeft = auto()
    ShiftRight = auto()

    def chars(self):
        if self == BinaryType.Add: return "+"
        elif self == BinaryType.Subtract: return "-"
        elif self == BinaryType.Multiply: return "*"
        elif self == BinaryType.Divide: return "/"
        elif self == BinaryType.Modolus: return "%"
        elif self == BinaryType.Power: return "**"
        elif self == BinaryType.And: return "&"
        elif self == BinaryType.Or: return "|"
        elif self == BinaryType.Xor: return "^"
        elif self == BinaryType.ShiftLeft: return "<<"
        elif self == BinaryType.ShiftRight: return ">>"
        else: raise Exception("unexhaustive map")

    def json_name(self):
        if self == BinaryType.Add: return "add"
        elif self == BinaryType.Subtract: return "subtract"
        elif self == BinaryType.Multiply: return "multiply"
        elif self == BinaryType.Divide: return "divide"
        elif self == BinaryType.Modolus: return "modolus"
        elif self == BinaryType.Power: return "power"
        elif self == BinaryType.And: return "and"
        elif self == BinaryType.Or: return "or"
        elif self == BinaryType.Xor: return "xor"
        elif self == BinaryType.ShiftLeft: return "shiftLeft"
        elif self == BinaryType.ShiftRight: return "shiftRight"
        else: raise Exception("unexhaustive map")

class Binary(Expr):
    def __init__(self, left: Expr, right: Expr, binary_type: BinaryType) -> None:
        self.expr_type = ExprType.Binary
        self.left = left
        self.right = right
        self.binary_type = binary_type
        super().__init__()

    def __str__(self) -> str:
        return f"({self.left} {self.binary_type.chars()} {self.right})"

    def to_json(self) -> str:
        return f'''{{
            "type": "expr",
            "exprType": "binary",
            "binaryType": "{self.binary_type.json_name()}",
            "left": {self.left.to_json()},
            "right": {self.right.to_json()}
        }}'''

class Not(Expr):
    def __init__(self, value: Expr) -> None:
        super().__init__()
        self.expr_type = ExprType.Not
        self.value = value

    def __str__(self) -> str:
        return f"(~{self.value})"

    def to_json(self) -> str:
        return f'''{{
            "type": "expr",
            "exprType": "not",
            "value": {self.value.to_json()}
        }}'''

class AtomExpr(Expr):
    def __init__(self, value: Atom) -> None:
        super().__init__()
        self.expr_type = ExprType.Atom
        self.value = value

    def __str__(self) -> str:
        return f"{self.value}"

    def to_json(self) -> str:
        return f'''{{
            "type": "expr",
            "exprType": "atom",
            "value": {self.value.to_json()}
        }}'''

class OperandType(Enum):
    Expr = auto()
    Deref = auto()
    Atom = auto()

class Operand:
    def __init__(self) -> None:
        self.operand_type: OperandType

    def __str__(self) -> str:
        raise NotImplementedError()

    def to_json(self) -> str:
        raise NotImplementedError()

class ExprOperand(Operand):
    def __init__(self, value: Expr) -> None:
        super().__init__()
        self.operand_type = OperandType.Expr
        self.value = value

    def __str__(self) -> str:
        return f"({self.value})"

    def to_json(self) -> str:
        return f'''{{
            "type": "operand",
            "operandType": "expr",
            "value": {self.value.to_json()}
        }}'''

class DerefOperand(Operand):
    def __init__(self, value: Expr) -> None:
        super().__init__()
        self.operand_type = OperandType.Deref
        self.value = value

    def __str__(self) -> str:
        return f"[{self.value}]"

    def to_json(self) -> str:
        return f'''{{
            "type": "operand",
            "operandType": "deref",
            "value": {self.value.to_json()}
        }}'''

class AtomOperand(Operand):
    def __init__(self, value: Atom) -> None:
        super().__init__()
        self.operand_type = OperandType.Atom
        self.value = value

    def __str__(self) -> str:
        return f"{self.value}"

    def to_json(self) -> str:
        return f'''{{
            "type": "operand",
            "operandType": "atom",
            "value": {self.value.to_json()}
        }}'''

class Operation:
    def __init__(self, operator: str, operands: List[Operand]) -> None:
        self.operator = operator
        self.operands = operands

    def __str__(self) -> str:
        return f"{self.operator} {', '.join(str(o) for o in self.operands)}"

    def to_json(self) -> str:
        operands = ", ".join([o.to_json() for o in self.operands])
        return f'''{{
            "type": "operation",
            "operator": "{self.operator}",
            "operands": [ {operands} ]
        }}'''

class Line:
    def __init__(self, label: Optional[str], operation: Optional[Operation], line_number: int) -> None:
        self.label = label
        self.operation = operation
        self.line_number = line_number

    def to_json(self) -> str:
        label = f"\"{self.label}\"" if self.label else 'null'
        operation = self.operation.to_json() if self.operation else 'null'
        return f'''{{
            "type": "line",
            "label": {label},
            "operation": {operation},
            "lineNumbr": {self.line_number}
        }}'''

class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.i = 0

    def step(self) -> None:
        self.i += 1

    def current(self) -> Token:
        return self.tokens[self.i]

    def current_type(self) -> TokenType:
        return self.current().type

    def current_is(self, type: TokenType) -> bool:
        return self.current_type() == type

    def assert_current(self, type: TokenType):
        if not self.current_is(type):
            raise Exception(
                f"unexpected token {self.current()}, expected {type}")

    def done(self) -> bool:
        return (self.i >= len(self.tokens) 
            or self.current().type == TokenType.EOF)

    def parse_line(self, line_number: int) -> Line:
        label = self.maybe_parse_label()
        operation = self.maybe_parse_operation()
        return Line(label, operation, line_number)

    def maybe_parse_label(self) -> Optional[str]:
        if self.current_is(TokenType.Name):
            value = self.current().value
            self.step()
            if self.current_is(TokenType.Colon):
                self.step()
                return value
            else:
                self.i -= 1
                return None
        else:
            return None

    def maybe_parse_operation(self) -> Optional[Operation]:
        if self.done(): return None
        self.assert_current(TokenType.Name)
        operator = self.current().value
        self.step()
        operands: List[Operand] = []
        if not self.done():
            operands.append(self.parse_operand())
            while not self.done():
                self.assert_current(TokenType.Comma)
                self.step()
                operands.append(self.parse_operand())
        return Operation(operator, operands)

    def parse_operand(self) -> Operand:
        if self.current_is(TokenType.LParen):
            value = self.parse_expression()
            return ExprOperand(value)
        elif self.current_is(TokenType.LBracket):
            self.step()
            value = self.parse_expression()
            self.assert_current(TokenType.RBracket)
            self.step()
            return DerefOperand(value)
        else:
            return AtomOperand(self.parse_atom())

    def parse_expression(self) -> Expr:
        if self.current_is(TokenType.Exclamation):
            self.step()
            value = self.parse_expression()
            return Not(value)
        else:
            left = self.parse_group()
            if self.current_is(TokenType.DoubleAsterisk):
                return self.make_binary(left, BinaryType.Power)
            elif self.current_is(TokenType.Asterisk):
                return self.make_binary(left, BinaryType.Multiply)
            elif self.current_is(TokenType.Slash):
                return self.make_binary(left, BinaryType.Divide)
            elif self.current_is(TokenType.Percent):
                return self.make_binary(left, BinaryType.Modolus)
            elif self.current_is(TokenType.Plus):
                return self.make_binary(left, BinaryType.Add)
            elif self.current_is(TokenType.Minus):
                return self.make_binary(left, BinaryType.Subtract)
            elif self.current_is(TokenType.DoubleLT):
                return self.make_binary(left, BinaryType.ShiftLeft)
            elif self.current_is(TokenType.DoubleGT):
                return self.make_binary(left, BinaryType.ShiftRight)
            elif self.current_is(TokenType.Ampersand):
                return self.make_binary(left, BinaryType.And)
            elif self.current_is(TokenType.Hat):
                return self.make_binary(left, BinaryType.Xor)
            elif self.current_is(TokenType.Pipe):
                return self.make_binary(left, BinaryType.Or)
            else:
                return left

    def make_binary(self, left: Expr, binary_type: BinaryType):
        self.step()
        right = self.parse_expression()
        return Binary(left, right, binary_type)

    def parse_group(self) -> Expr:
        if self.current_is(TokenType.LParen):
            self.step()
            value = self.parse_expression()
            self.assert_current(TokenType.RParen)
            self.step()
            return value
        else:
            return AtomExpr(self.parse_atom())

    def parse_atom(self) -> Atom:
        if self.current_is(TokenType.Name):
            value = self.current().value
            self.step()
            return Name(value)
        elif self.current_is(TokenType.Int):
            value = self.current().value
            self.step()
            return Int(value)
        elif self.current_is(TokenType.Hex):
            value = self.current().value
            self.step()
            return Hex(value)
        else:
            raise Exception(f"expected atom, got {self.current()}")

def parse_lines(text: str) -> List[Line]:
    parsed_lines: List[Line] = []
    for i, line in enumerate(text.split("\n")):
        if line == "": continue
        tokens = tokenize(line)
        if len(tokens) <= 1: continue
        parsed_lines.append(Parser(tokens).parse_line(i))
    return parsed_lines
