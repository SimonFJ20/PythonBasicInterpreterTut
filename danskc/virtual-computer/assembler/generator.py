from typing import List, cast
from assembler.parser import AtomExpr, AtomOperand, AtomType, Binary, BinaryType, DerefOperand, ExprOperand, Expr, ExprType, Int, Line, Name, Not, Operand, OperandType, Operation, parse_lines
from assembler.symbols import SymbolTable, find_symbols, instruction_size
from assembler.checker import check_operation, is_register
from assembler.spec import PROGRAM_START

def evaluate_expression(expr: Expr, symbols: SymbolTable, lc: int) -> int:
    if expr.expr_type == ExprType.Binary:
        binary = cast(Binary, expr)
        left = evaluate_expression(binary.left, symbols, lc)
        right = evaluate_expression(binary.right, symbols, lc)
        if binary.binary_type == BinaryType.Add:            return left + right
        elif binary.binary_type == BinaryType.Subtract:     return left - right
        elif binary.binary_type == BinaryType.Multiply:     return left * right
        elif binary.binary_type == BinaryType.Divide:       return int(left / right)
        elif binary.binary_type == BinaryType.Modolus:      return left % right
        elif binary.binary_type == BinaryType.Power:        return left ** right
        elif binary.binary_type == BinaryType.And:          return left & right
        elif binary.binary_type == BinaryType.Or:           return left | right
        elif binary.binary_type == BinaryType.Xor:          return left ^ right
        elif binary.binary_type == BinaryType.ShiftLeft:    return left << right
        elif binary.binary_type == BinaryType.ShiftRight:   return left >> right
        else: raise Exception("unexhaustive match")
    elif expr.expr_type == ExprType.Not:
        not_expr = cast(Not, expr)
        return not evaluate_expression(not_expr.value, symbols, lc)
    elif expr.expr_type == ExprType.Atom:
        atom = cast(AtomExpr, expr).value
        if atom.atom_type == AtomType.Name:
            return symbols.get(cast(Name, atom).value, lc)
        elif atom.atom_type == AtomType.Int:
            return cast(Int, atom).value
        elif atom.atom_type == AtomType.Hex:
            return cast(Int, atom).value
        else:
            raise Exception("unexhaustive match")
    else:
        raise Exception("unexhaustive match")

def generate_operand(operand: Operand, symbols: SymbolTable, lc: int) -> str:
    if operand.operand_type == OperandType.Expr:
        return f"{evaluate_expression(cast(ExprOperand, operand).value, symbols, lc)}"
    elif operand.operand_type == OperandType.Deref:
        return f"&{evaluate_expression(cast(ExprOperand, operand).value, symbols, lc)}"
    elif operand.operand_type == OperandType.Atom:
        atom = cast(AtomOperand, operand).value
        if atom.atom_type == AtomType.Name:
            name = cast(Name, atom).value
            if is_register(name):
                return name
            else:
                return str(symbols.get(name, lc))
        elif atom.atom_type == AtomType.Int:
            return str(cast(Int, atom).value)
        elif atom.atom_type == AtomType.Hex:
            return str(cast(Int, atom).value)
        else:
            raise Exception("unexhaustive match")
    else:
        raise Exception("unexhaustive match")

def generate_operation(operation: Operation, symbols: SymbolTable, lc: int) -> str:
    operator = operation.operator
    operands = " ".join(map(lambda operand: generate_operand(operand, symbols, lc), operation.operands))
    return f"{operator} {operands}"

def generate_operations(operations: List[Operation], symbols: SymbolTable, debug: bool) -> str:
    generated_lines: List[str] = []
    lc = PROGRAM_START
    for operation in operations:
        if debug:
            generated_lines.append(f"; {lc}: {operation}")
        generated_lines.append(generate_operation(operation, symbols, lc))
        lc += instruction_size(operation.operator)
    return "\n".join(generated_lines)

def generate_lines(lines: List[Line], symbols: SymbolTable, debug: bool) -> str:
    operations = [line.operation for line in lines if line.operation]
    return generate_operations(operations, symbols, debug)
