from typing import List, cast
from assembler.parser import (AtomExpr, AtomOperand, AtomType, Binary,
                              DerefOperand, ExprOperand, Expr, ExprType, Hex,
                              Int, Line, Name, Not, Operand, OperandType,
                              Operation, parse_lines)
from assembler.symbols import SymbolTable, find_symbols


def checker_error(message: str, line_number: int) -> None:
    raise Exception(f"checker error on line {line_number + 1}:\n{message}\n")

def check_operand_count(operation: Operation, line_number: int, expected_count: int) -> None:
    if len(operation.operands) != expected_count:
        checker_error(
            f"\"{operation.operator}\" expects {expected_count} operands, got {len(operation.operands)}",
            line_number,
        )

def is_register(name: str) -> bool:
    return name in ["ra", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8"]

def check_expression(expr: Expr, symbols: SymbolTable, line_number: int) -> None:
    if expr.expr_type == ExprType.Binary:
        binary = cast(Binary, expr)
        check_expression(binary.left, symbols, line_number)
        check_expression(binary.right, symbols, line_number)
    elif expr.expr_type == ExprType.Not:
        not_expr = cast(Not, expr)
        check_expression(not_expr.value, symbols, line_number)
    elif expr.expr_type == ExprType.Atom:
        atom = cast(AtomExpr, expr).value
        if atom.atom_type == AtomType.Name:
            name_atom = cast(Name, atom)
            if not symbols.is_defined(name_atom.value) and not is_register(name_atom.value):
                checker_error(f"symbol \"{name_atom.value}\" is not defined", line_number)
    else:
        raise Exception("unexhaustive match")

def check_address(operation: Operation, i: int, symbols: SymbolTable, line_number: int) -> None:
    operand = operation.operands[i]
    if operand.operand_type == OperandType.Expr:
        checker_error(f"expected address as operand {i+1} of \"{operation.operator}\" instruction", line_number)
    elif operand.operand_type == OperandType.Deref:
        check_expression(cast(DerefOperand, operand).value, symbols, line_number)
    elif operand.operand_type == OperandType.Atom:
        atom = cast(AtomOperand, operand).value
        if atom.atom_type == AtomType.Name:
            name_atom = cast(Name, atom)
            if not symbols.is_defined(name_atom.value) and not is_register(name_atom.value):
                checker_error(f"symbol \"{name_atom.value}\" is not defined", line_number)
        else:
            checker_error(f"expected address as operand {i+1} of \"{operation.operator}\" instruction", line_number)
    else:
        raise Exception("unexhaustive match")

def check_value(operation: Operation, i: int, symbols: SymbolTable, line_number: int) -> None:
    operand = operation.operands[i]
    if operand.operand_type == OperandType.Expr:
        check_expression(cast(ExprOperand, operand).value, symbols, line_number)
    elif operand.operand_type == OperandType.Deref:
        checker_error(f"expected expression as operand {i+1} of \"{operation.operator}\" instruction", line_number)
    elif operand.operand_type == OperandType.Atom:
        atom = cast(AtomOperand, operand).value
        if atom.atom_type == AtomType.Name:
            name_atom = cast(Name, atom)
            if not symbols.is_defined(name_atom.value):
                checker_error(f"symbol \"{name_atom.value}\" is not defined", line_number)
    else:
        raise Exception("unexhaustive match")

def check_address_or_value(operation: Operation, i: int, symbols: SymbolTable, line_number: int) -> None:
    operand = operation.operands[i]
    if operand.operand_type == OperandType.Expr:
        check_expression(cast(ExprOperand, operand).value, symbols, line_number)
    elif operand.operand_type == OperandType.Deref:
        check_expression(cast(DerefOperand, operand).value, symbols, line_number)
    elif operand.operand_type == OperandType.Atom:
        atom = cast(AtomOperand, operand).value
        if atom.atom_type == AtomType.Name:
            name_atom = cast(Name, atom)
            if not symbols.is_defined(name_atom.value) and not is_register(name_atom.value):
                checker_error(f"symbol \"{name_atom.value}\" is not defined", line_number)
    else:
        raise Exception("unexhaustive match")


def check_operation(operation: Operation, symbols: SymbolTable, line_number: int) -> None:
    if operation.operator == "noop":
        check_operand_count(operation, line_number, 0)

    elif operation.operator == "jmp":
        check_operand_count(operation, line_number, 1)
        check_address_or_value(operation, 0, symbols, line_number)

    elif operation.operator == "jnz":
        check_operand_count(operation, line_number, 2)
        check_address_or_value(operation, 0, symbols, line_number)
        check_address(operation, 1, symbols, line_number)

    elif operation.operator == "mov":
        check_operand_count(operation, line_number, 2)
        check_address(operation, 0, symbols, line_number)

    elif operation.operator == "load":
        check_operand_count(operation, line_number, 2)
        check_address(operation, 0, symbols, line_number)
        check_address(operation, 1, symbols, line_number)

    elif operation.operator == "store":
        check_operand_count(operation, line_number, 2)
        check_address(operation, 0, symbols, line_number)
        check_address(operation, 1, symbols, line_number)

    elif operation.operator in ["and", "or", "xor", "add", "sub", "mul", "div", "mod", "shl", "cmp", "lt"]:
        check_operand_count(operation, line_number, 2)
        check_address(operation, 0, symbols, line_number)
        check_address(operation, 1, symbols, line_number)
    
    else:
        checker_error(f"unknown instruction \"{operation.operator}\"", line_number)

def check_lines(lines: List[Line], symbols: SymbolTable) -> None:
    for line in lines:
        if not line.operation: continue
        check_operation(line.operation, symbols, line.line_number)
