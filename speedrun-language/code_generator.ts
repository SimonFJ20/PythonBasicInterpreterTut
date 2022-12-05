import { SymbolTable, Function, Type } from "./checker.ts";
import * as ast from "./ast.ts";
import { force, match, _ } from "./utils.ts";

export type Generator = {
    st: SymbolTable;
    functions: Function[];
};

export const generate = (self: Generator, program: ast.Statement[]): string => {
    const code =
        "#include <stdio.h>\n" +
        "#include <stdlib.h>\n" +
        "#include <stdint.h>\n" +
        "#include <stdbool.h>\n" +
        "#include <string.h>\n" +
        "int main()\n{\n" +
        generate_statements(self, program) +
        "\n}\n";
    return code;
};

const generate_statements = (
    self: Generator,
    nodes: ast.Statement[],
): string => {
    return nodes.map((node) => generate_statement(self, node)).join("\n");
};

const generate_statement = (self: Generator, node: ast.Statement): string => {
    // prettier-ignore
    return match(node.id, [
        ["ConstDefinition", () => generate_const_definition(self, force(node))],
        [_, () => {
            throw new Error(`code generation not implemented for statement '${node.id}'`);
        }]
    ]);
};

const generate_type = (self: Generator, type: Type): string => {
    // prettier-ignore
    return match(type.id, [
        ["FunctionType", () => "void*"],
        ["IntType", () => "int"],
        [_, () => {
            throw new Error(`code generation not implemented for type '${type.id}'`);
        }]
    ]);
};

const generate_const_definition = (
    self: Generator,
    node: ast.ConstDefinition,
): string => {
    const type = generate_type(
        self,
        self.st.get(node.target.name).expect("_").type,
    );
    const name = node.target.name;
    const value = generate_expression(self, node.value);
    return `${type} ${name} = ${value};`;
};

const generate_expression = (self: Generator, node: ast.Expression): string => {
    // prettier-ignore
    return match(node.id, [
        ["Function", () => generate_function(self, force(node))],
        ["BinaryOperation", () => generate_binary_operation(self, force(node))],
        ["Accessor", () => generate_accessor(force(node))],
        ["Int", () => generate_int(force(node))],
        [_, () => {
            throw new Error(`code generation not implemented for expression '${node.id}'`);
        }]
    ]);
};

const generate_function = (self: Generator, node: ast.Function): string => {
    // instead of checker(ast) -> ast + total perspective symbol table
    // do checker(ast) -> checked(ast) + node specific symbol table
    throw new Error("_");
};

const generate_binary_operation = (
    self: Generator,
    node: ast.BinaryOperation,
): string => {
    const operator = match(node.operation, [
        [ast.OperationType.Add, () => "+"],
        [ast.OperationType.Subtract, () => "-"],
        [ast.OperationType.Multiply, () => "*"],
        [ast.OperationType.Divide, () => "/"],
        [ast.OperationType.Modulus, () => "%"],
    ]);
    const left = generate_expression(self, node.left);
    const right = generate_expression(self, node.right);
    return `(${left} ${operator} ${right})`;
};

const generate_accessor = (node: ast.Accessor): string => node.name;

const generate_int = (node: ast.Int): string => node.value.toString();
