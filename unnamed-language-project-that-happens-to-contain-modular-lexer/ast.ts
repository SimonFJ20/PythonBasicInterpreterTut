import { Span, Token, Position } from "./lexer.ts";
import { TokenType } from "./tokentypes.ts";

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
    public constructor(public value: Token<TokenType>) {
        super(TypeType.TypeName, value.span);
    }
}

export abstract class ExpressionNode extends ParseNode {
    protected constructor(public type: ExpressionType, span: Span) {
        super(span);
    }
}

export class LetDeclarationNode extends ExpressionNode {
    public constructor(
        public target: Token<TokenType>,
        public value: ExpressionNode,
        begin: Position,
    ) {
        super(ExpressionType.LetDeclaration, new Span(begin, value.span.end));
    }
}

export class MutDeclarationNode extends ExpressionNode {
    public constructor(
        public target: Token<TokenType>,
        public value: ExpressionNode,
        begin: Position,
    ) {
        super(ExpressionType.MutDeclaration, new Span(begin, value.span.end));
    }
}

export class Function extends ExpressionNode {
    public constructor(
        public args: Token<TokenType>,
        public body: ExpressionNode,
        span: Span,
    ) {
        super(ExpressionType.Function, span);
    }
}

export class AssignmentNode extends ExpressionNode {
    public constructor(
        public target: Token<TokenType>,
        public value: ExpressionNode,
    ) {
        super(
            ExpressionType.Assignment,
            new Span(target.span.begin, value.span.end),
        );
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
    public constructor(public value: Token<TokenType>) {
        super(ExpressionType.IntLiteral, value.span);
    }
}

export class CharLiteralNode extends ExpressionNode {
    public constructor(public value: Token<TokenType>) {
        super(ExpressionType.CharLiteral, value.span);
    }
}

export class StringLiteralNode extends ExpressionNode {
    public constructor(public value: Token<TokenType>) {
        super(ExpressionType.StringLiteral, value.span);
    }
}
