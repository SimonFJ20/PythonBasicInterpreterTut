import unittest
from nodes import *
from interpreter import Interpreter
from values import Number

class TestInterpreters(unittest.TestCase):

    def test_numbers(self):
        value = Interpreter().visit(NumberNode(51.2))
        self.assertEqual(value, Number(51.2))

    def test_add_operation(self):
        value = Interpreter().visit(
            AddNode(
                NumberNode(12),
                NumberNode(34)
            )
        )
        self.assertEqual(value, Number(12 + 34))

    def test_subtract_operation(self):
        value = Interpreter().visit(
            SubtractNode(
                NumberNode(12),
                NumberNode(34)
            )
        )
        self.assertEqual(value, Number(12 - 34))

    def test_multiply_operation(self):
        value = Interpreter().visit(
            MultiplyNode(
                NumberNode(12),
                NumberNode(34)
            )
        )
        self.assertEqual(value, Number(12 * 34))

    def test_divide_operation(self):
        value = Interpreter().visit(
            DivideNode(
                NumberNode(12),
                NumberNode(34)
            )
        )
        self.assertEqual(value, Number(12 / 34))

    def test_divide_by_zero(self):
        with self.assertRaises(Exception):
            Interpreter().visit(
                DivideNode(
                    NumberNode(10),
                    NumberNode(0)
                )
            )
        
    def test_full_expression(self):
        value = Interpreter().visit(
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
        self.assertEqual(value, Number((2 * 3 + 4) / -((2 * 3) - 4)))
