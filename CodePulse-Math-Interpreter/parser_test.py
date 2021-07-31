import unittest
from tokens import Token, TokenType
from parser_ import Parser
from nodes import *

class TestParser(unittest.TestCase):

    def test_empty(self):
        tokens = []
        node = Parser(tokens).parse()
        self.assertEqual(node, None)

    def test_numbers(self):
        tokens = [Token(TokenType.NUMBER, 12.34)]
        node = Parser(tokens).parse()
        self.assertEqual(node, NumberNode(12.34))

    def test_add_operation(self):
        tokens = [
            Token(TokenType.NUMBER, 12),
            Token(TokenType.PLUS),
            Token(TokenType.NUMBER, 34),
        ]
        node = Parser(tokens).parse()
        self.assertEqual(node, AddNode(NumberNode(12), NumberNode(34)))
    
    def test_subtract_operation(self):
        tokens = [
            Token(TokenType.NUMBER, 12),
            Token(TokenType.MINUS),
            Token(TokenType.NUMBER, 34),
        ]
        node = Parser(tokens).parse()
        self.assertEqual(node, SubtractNode(NumberNode(12), NumberNode(34)))
    
    def test_multiply_operation(self):
        tokens = [
            Token(TokenType.NUMBER, 12),
            Token(TokenType.MULTIPLY),
            Token(TokenType.NUMBER, 34),
        ]
        node = Parser(tokens).parse()
        self.assertEqual(node, MultiplyNode(NumberNode(12), NumberNode(34)))
    
    def test_divide_operation(self):
        tokens = [
            Token(TokenType.NUMBER, 12),
            Token(TokenType.DIVIDE),
            Token(TokenType.NUMBER, 34),
        ]
        node = Parser(tokens).parse()
        self.assertEqual(node, DivideNode(NumberNode(12), NumberNode(34)))
    
    def test_full_expression(self):
        tokens = [
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
        ]
        node = Parser(tokens).parse()
        self.assertEqual(node, 
            DivideNode(
                AddNode(
                    MultiplyNode(
                        NumberNode(2.0),
                        NumberNode(3.0)
                    ),
                    NumberNode(4.0)
                ),
                MinusNode(
                    SubtractNode(
                        MultiplyNode(
                            NumberNode(2.0),
                            NumberNode(3.0)
                        ),
                        NumberNode(4.0)
                    )
                )
            )
        )

