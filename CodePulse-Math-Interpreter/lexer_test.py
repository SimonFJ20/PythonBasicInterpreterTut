import unittest
from tokens import Token, TokenType
from lexer import Lexer

class TestLexer(unittest.TestCase):

    def test_empty(self):
        tokens = list(Lexer('').generate_tokens())
        self.assertEqual(tokens, [])
    
    def test_empty(self):
        tokens = list(Lexer(' \t\t \n \t\n\n\t ').generate_tokens())
        self.assertEqual(tokens, [])

    def test_numbers(self):
        tokens = list(Lexer('123 123.456 123. .546 .').generate_tokens())
        self.assertEqual(tokens, [
            Token(TokenType.NUMBER, 123.0),
            Token(TokenType.NUMBER, 123.456),
            Token(TokenType.NUMBER, 123.0),
            Token(TokenType.NUMBER, 0.546),
            Token(TokenType.NUMBER, 0.)
        ])

    def test_operators(self):
        tokens = list(Lexer('+-*/').generate_tokens())
        self.assertEqual(tokens, [
            Token(TokenType.PLUS),
            Token(TokenType.MINUS),
            Token(TokenType.MULTIPLY),
            Token(TokenType.DIVIDE),
        ])

    def test_parens(self):
        tokens = list(Lexer('()').generate_tokens())
        self.assertEqual(tokens, [
            Token(TokenType.LPAREN),
            Token(TokenType.RPAREN),
        ])

    def test_full_expression(self):
        tokens = list(Lexer('(2 * 3 + 4) / -((2 * 3) - 4)').generate_tokens())
        self.assertEqual(tokens, [
            Token(TokenType.LPAREN),
            Token(TokenType.NUMBER, 2.0),
            Token(TokenType.MULTIPLY),
            Token(TokenType.NUMBER, 3.0),
            Token(TokenType.PLUS),
            Token(TokenType.NUMBER, 4.0),
            Token(TokenType.RPAREN),
            Token(TokenType.DIVIDE),
            Token(TokenType.MINUS),
            Token(TokenType.LPAREN),
            Token(TokenType.LPAREN),
            Token(TokenType.NUMBER, 2.0),
            Token(TokenType.MULTIPLY),
            Token(TokenType.NUMBER, 3.0),
            Token(TokenType.RPAREN),
            Token(TokenType.MINUS),
            Token(TokenType.NUMBER, 4.0),
            Token(TokenType.RPAREN),
        ])
