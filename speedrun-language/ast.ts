import { id_generator, Option } from "./utils.ts";

export abstract class Node {
    protected constructor(public id: string) {}
}

export abstract class Statement extends Node {}

export class Block extends Statement {
    public constructor(public body: Statement[]) {
        super("Block");
    }
}

export class ConstDefinition extends Statement {
    public constructor(public target: Argument, public value: Expression) {
        super("ConstDefinition");
    }
}

export class LetDeclaration extends Statement {
    public constructor(
        public target: Argument,
        public value: Option<Expression>,
    ) {
        super("LetDeclaration");
    }
}

export class If extends Statement {
    public constructor(public condition: Expression, public body: Statement) {
        super("If");
    }
}

export class IfElse extends Statement {
    public constructor(
        public condition: Expression,
        public truhty: Statement,
        public falsy: Statement,
    ) {
        super("IfElse");
    }
}

export class While extends Statement {
    public constructor(public condition: Expression, public body: Statement) {
        super("While");
    }
}

export class ExpressionStatement extends Statement {
    public constructor(public expression: Expression) {
        super("ExpressionStatement");
    }
}

export abstract class Type extends Node {}

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

export abstract class Expression extends Node {}

export class Function extends Expression {
    private static fid_generator = id_generator();
    public fid = Function.fid_generator();

    public constructor(
        public args: Argument[],
        public return_type: Option<Type>,
        public body: Statement,
    ) {
        super("Function");
    }
}

export class Argument extends Node {
    public constructor(public name: string, public type: Type) {
        super("Argument");
    }
}

export enum OperationType {
    Add,
    Subtract,
    Multiply,
    Divide,
    Modulus,
}

export class BinaryOperation extends Expression {
    public constructor(
        public operation: OperationType,
        public left: Value,
        public right: Value,
    ) {
        super("BinaryOperation");
    }
}

export class Call extends Expression {
    public constructor(public callee: Expression, public args: Expression[]) {
        super("Call");
    }
}

export abstract class Value extends Expression {}

export class Int extends Value {
    public constructor(public value: number) {
        super("Int");
    }
}

export class String extends Value {
    public constructor(public value: string) {
        super("String");
    }
}

export class Accessor extends Value {
    public constructor(public name: string) {
        super("Accessor");
    }
}
