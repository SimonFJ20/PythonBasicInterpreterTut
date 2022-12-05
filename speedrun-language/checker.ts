import * as ast from "./ast.ts";
import { Err, force, match, Ok, Or, qmark, Result, _ } from "./utils.ts";

export abstract class Type {
    protected constructor(public id: string) {}
}

export class VoidType extends Type {
    public constructor() {
        super("VoidType");
    }
}

export class IntType extends Type {
    public constructor() {
        super("IntType");
    }
}

export class StringType extends Type {
    public constructor() {
        super("StringType");
    }
}

export class FunctionType extends Type {
    public constructor(public args: Type[], public return_type: Type) {
        super("FunctionType");
    }
}

const types_compatible = (a: Type, b: Type): boolean => {
    // prettier-ignore
    return match(a.id, [
        ["VoidType", () => b.id === "VoidType"],
        ["IntType", () => b.id === "IntType"],
        ["FunctionType", () => match(b.id, [
            ["FunctionType", () => function_types_compatible(force(a), force(b))],
            [_, () => false]
        ])],
        [_, () => {
            throw new Error(
                `types_compatible unexhaustive '${a.id}' and '${b.id}'`,
            );
        }]
    ]);
};

const function_types_compatible = (
    a: FunctionType,
    b: FunctionType,
): boolean => {
    if (a.args.length !== b.args.length) return false;
    else return true;
};

export type Symbol = {
    name: string;
    type: Type;
    mutable: boolean;
};

export class SymbolTable {
    private symbols = new Map<string, Symbol>();
    private children: SymbolTable[] = [];

    public constructor(private parent: SymbolTable | null = null) {}

    public add_child(child: SymbolTable) {
        this.children.push(child);
    }

    public declared_locally(name: string): boolean {
        return this.symbols.has(name);
    }

    public declared(name: string): boolean {
        return (
            this.declared_locally(name) ||
            (this.parent?.declared(name) ?? false)
        );
    }

    public get_locally(name: string): Result<Symbol, string> {
        const symbol = this.symbols.get(name);
        return symbol ? Ok(symbol) : Err("cannot find symbol");
    }

    public get(name: string): Result<Symbol, string> {
        return this.get_locally(name).match(
            (v) => Ok(v),
            (e) => (this.parent ? this.parent.get(name) : Err(e)),
        );
    }

    public set(symbol: Symbol) {
        this.symbols.set(symbol.name, symbol);
    }
}

export type Function = {
    id: number;
    node: ast.Function;
    type: FunctionType;
    symbol_table: SymbolTable;
};

export type CheckerError = string;

export type CheckerResult = {
    st: SymbolTable;
    functions: Function[];
    errors: CheckerError[];
};

export class Checker {
    private symbol_table!: SymbolTable;
    private symbol_table_history!: SymbolTable[];
    private functions!: Function[];
    private errors!: CheckerError[];

    public check_program(program: ast.Statement[]): CheckerResult {
        this.symbol_table = new SymbolTable();
        this.symbol_table_history = [];
        this.functions = [];
        this.errors = [];
        this.check_statements(program);
        return {
            st: this.symbol_table,
            functions: this.functions,
            errors: this.errors,
        };
    }

    public check_statements(nodes: ast.Statement[]): Type {
        return (
            nodes
                .map((v) =>
                    this.check_statement(v).match(
                        (v) => v,
                        (e) => {
                            this.errors.push(e);
                            return null;
                        },
                    ),
                )
                .find((v) => v && v.id !== "VoidType") ?? new VoidType()
        );
    }

    public check_statement(node: ast.Statement): Result<Type, CheckerError> {
        switch (node.id) {
            case "Block":
                return Ok(this.check_block(force(node)));
            case "ConstDefinition":
                return this.check_const_definition(force(node));
            case "ExpressionStatement":
                return this.check_expression_statement(force(node));
            default:
                throw new Error(`unchecked statement '${node.id}'`);
        }
    }

    public check_block(node: ast.Block): Type {
        this.branch_symbol_table();
        const type = this.check_statements(node.body);
        this.merge_symbol_table();
        return type;
    }

    public check_const_definition(
        node: ast.ConstDefinition,
    ): Result<Type, CheckerError> {
        if (this.symbol_table.declared_locally(node.target.name))
            return Err(`multiple definitions of symbol '${node.target.name}'`);
        const value_type_result = this.check_expression(node.value);
        if (value_type_result.is_err()) return value_type_result.transform();
        const value_type = value_type_result.unwrap();
        if (node.target.type && !types_compatible(node.target.type, value_type))
            return Err("types incompatible");
        this.symbol_table.set({
            name: node.target.name,
            type: value_type,
            mutable: false,
        });
        return Ok(new VoidType());
    }

    public check_expression_statement(
        node: ast.ExpressionStatement,
    ): Result<Type, CheckerError> {
        this.check_expression(node.expression);
        return Ok(new VoidType());
    }

    public check_expression(node: ast.Expression): Result<Type, CheckerError> {
        switch (node.id) {
            case "Function":
                return this.check_function(force(node));
            case "BinaryOperation":
                return this.check_binary_operation(force(node));
            case "Call":
                return this.check_call(force(node));
            case "Accessor":
                return this.check_accessor(force(node));
            case "Int":
                return Ok(new IntType());
            default:
                throw new Error(`unchecked expression '${node.id}'`);
        }
    }

    public check_function(node: ast.Function): Result<Type, CheckerError> {
        this.branch_symbol_table();
        for (const arg of node.args) {
            if (!this.symbol_table.declared_locally(arg.name))
                this.symbol_table.set({
                    name: arg.name,
                    type: arg.type,
                    mutable: true,
                });
            else return Err(`multiple definitions of argument '${arg.name}'`);
        }
        this.branch_symbol_table();
        const decl_return_type = node.return_type.match(
            (v) => this.check_type(v).expect("_"),
            () => new VoidType(),
        );
        const body_return_type_result = this.check_statement(node.body);
        if (!body_return_type_result.is_ok())
            return body_return_type_result.transform();
        const body_return_type =
            body_return_type_result.unwrap() ?? new VoidType();
        if (!types_compatible(decl_return_type, body_return_type))
            return Err("incompatible returntypes");
        this.merge_symbol_table();
        this.merge_symbol_table();
        const type = new FunctionType(
            node.args.map((arg) => this.check_type(arg.type).expect("_")),
            decl_return_type,
        );
        this.functions.push({
            id: node.fid,
            node,
            type,
            symbol_table: this.symbol_table,
        });
        return Ok(type);
    }

    public check_binary_operation(
        node: ast.BinaryOperation,
    ): Result<Type, CheckerError> {
        return qmark(this.check_expression(node.left), (left_type) => {
            return qmark(this.check_expression(node.right), (right_type) => {
                const impossible_operation_string = () =>
                    `impossible operation: '${left_type.id} + ${right_type.id}'`;

                // prettier-ignore
                return match(node.operation, [
                    [ast.OperationType.Add, () => match(left_type.id, [
                        ["IntType", () => match(right_type.id, [
                            ["IntType", () => Ok(left_type)],
                            [_, () => Err(impossible_operation_string())], 
                        ])],
                        ["StringType", () => match(right_type.id, [
                            ["StringType", () => Ok(left_type)],
                            [_, () => Err(impossible_operation_string())], 
                        ])],
                        [_, () => Err(impossible_operation_string())],
                    ])],
                    [ast.OperationType.Subtract, Or],
                    [ast.OperationType.Multiply, Or],
                    [ast.OperationType.Divide, Or],
                    [ast.OperationType.Modulus, () => match(left_type.id, [
                        ["IntType", () => match(right_type.id, [
                            ["IntType", () => Ok(left_type)],
                            [_, () => Err(impossible_operation_string())], 
                        ])],
                        [_, () => Err(impossible_operation_string())],
                    ])],
                ]);
            });
        });
    }

    public check_call(node: ast.Call): Result<Type, CheckerError> {
        const callee_type_result = this.check_expression(node.callee);
        if (!callee_type_result.is_ok()) return callee_type_result.transform();
        const callee_type = callee_type_result.unwrap() as FunctionType;
        if (callee_type.id !== "FunctionType")
            return Err("cannot call non-function type");
        else if (callee_type.args.length !== node.args.length)
            return Err("wrong amount of arguments");
        else return Ok(callee_type.return_type);
    }

    public check_accessor(node: ast.Accessor): Result<Type, CheckerError> {
        const symbol = this.symbol_table
            .get(node.name)
            .expect(`symbol to be declared '${node.name}'`);
        return Ok(symbol.type);
    }

    public check_type(node: ast.Type): Result<Type, CheckerError> {
        switch (node.id) {
            case "IntType":
                return Ok(new IntType());
            default:
                throw new Error(`unchecked type '${node.id}'`);
        }
    }

    private branch_symbol_table() {
        this.symbol_table_history.push(this.symbol_table);
        this.symbol_table = new SymbolTable(this.symbol_table);
    }

    private merge_symbol_table() {
        const symbol_table = this.symbol_table_history.pop();
        if (!symbol_table) throw new Error("no symbol table history");
        symbol_table.add_child(this.symbol_table);
        this.symbol_table = symbol_table;
    }
}
