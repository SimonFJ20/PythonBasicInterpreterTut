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
    ThinArrow = auto()
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
        return f'{{ tt: {self.tt}, value: "{self.value}", row: {self.line} }}'


def chars_match(pool: str, matcher: str) -> bool:
    if len(pool) < len(matcher):
        return False
    for i, v in enumerate(matcher):
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
        if text[i] in " \t\r\n":
            if text[i] == "\n":
                line += 1
            i += 1
        elif chars_match(text[i:], "KOMMENTAR"):
            while i < len(text) and text[i] != "\n":
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
            if i >= len(text):
                raise Exception("unfinished char literal")
            if text[i] == "\n":
                line += 1
            value += text[i]
            if text[i] == "\\":
                i += 1
                if i >= len(text):
                    raise Exception("unfinished char literal")
                value += text[i]
            i += 1
            if i >= len(text) or text[i] != "'":
                raise Exception("unfinished char literal")
            value += text[i]
            i += 1
            tokens.append(Token(TokenTypes.Char, value, line))
        elif text[i] == '"':
            value = text[i]
            i += 1
            escaped = False
            while i < len(text):
                if escaped:
                    escaped = False
                else:
                    if text[i] == '"':
                        break
                    elif text[i] == "\\":
                        escaped = True
                if text[i] == "\n":
                    line += 1
                value += text[i]
                i += 1
            if text[i] != '"':
                raise Exception("unfinished string literal")
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
        elif chars_match(text[i:], "->"):
            tokens.append(Token(TokenTypes.ThinArrow, text[i : i + 2], line))
            i += 2
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
