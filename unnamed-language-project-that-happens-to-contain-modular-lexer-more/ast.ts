import { Span, Position } from "./lexer.ts";

export enum TypeType {
    TypeName,
}

export enum ExpressionType {
    LetDeclaration,
    MutDeclaration,
    Function,
    Assignment,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Remainder,
    IntLiteral,
    CharLiteral,
    StringLiteral,
}

export abstract class ParseNode {
    protected constructor(public span: Span) {}
}

export abstract class TypeNode extends ParseNode {
    protected constructor(public type: TypeType, span: Span) {
        super(span);
    }
}

export class TypeNameNode extends TypeNode {
    public constructor(public name: string, span: Span) {
        super(TypeType.TypeName, span);
    }
}

export abstract class ExpressionNode extends ParseNode {
    protected constructor(public type: ExpressionType, span: Span) {
        super(span);
    }
}

export class LetDeclarationNode extends ExpressionNode {
    public constructor(
        public identifier: string,
        public value: ExpressionNode,
        begin: Position,
    ) {
        super(ExpressionType.LetDeclaration, new Span(begin, value.span.end));
    }
}

export class MutDeclarationNode extends ExpressionNode {
    public constructor(
        public identifier: string,
        public value: ExpressionNode,
        begin: Position,
    ) {
        super(ExpressionType.MutDeclaration, new Span(begin, value.span.end));
    }
}

export class Function extends ExpressionNode {
    public constructor(
        public args: { identifier: string; type: TypeNode }[],
        public body: ExpressionNode,
        span: Span,
    ) {
        super(ExpressionType.Function, span);
    }
}

export class AssignmentNode extends ExpressionNode {
    public constructor(
        public identifier: string,
        public value: ExpressionNode,
        begin: Position,
    ) {
        super(ExpressionType.Assignment, new Span(begin, value.span.end));
    }
}

export class AdditionNode extends ExpressionNode {
    public constructor(
        public left: ExpressionNode,
        public right: ExpressionNode,
    ) {
        super(
            ExpressionType.Addition,
            new Span(left.span.begin, right.span.end),
        );
    }
}

export class SubtractionNode extends ExpressionNode {
    public constructor(
        public left: ExpressionNode,
        public right: ExpressionNode,
    ) {
        super(
            ExpressionType.Subtraction,
            new Span(left.span.begin, right.span.end),
        );
    }
}

export class MultiplicationNode extends ExpressionNode {
    public constructor(
        public left: ExpressionNode,
        public right: ExpressionNode,
    ) {
        super(
            ExpressionType.Multiplication,
            new Span(left.span.begin, right.span.end),
        );
    }
}

export class DivisionNode extends ExpressionNode {
    public constructor(
        public left: ExpressionNode,
        public right: ExpressionNode,
    ) {
        super(
            ExpressionType.Division,
            new Span(left.span.begin, right.span.end),
        );
    }
}

export class RemainderNode extends ExpressionNode {
    public constructor(
        public left: ExpressionNode,
        public right: ExpressionNode,
    ) {
        super(
            ExpressionType.Remainder,
            new Span(left.span.begin, right.span.end),
        );
    }
}

export class IntLiteralNode extends ExpressionNode {
    public constructor(public value: string, span: Span) {
        super(ExpressionType.IntLiteral, span);
    }
}

export class CharLiteralNode extends ExpressionNode {
    public constructor(public value: string, span: Span) {
        super(ExpressionType.CharLiteral, span);
    }
}

export class StringLiteralNode extends ExpressionNode {
    public constructor(public value: string, span: Span) {
        super(ExpressionType.StringLiteral, span);
    }
}
