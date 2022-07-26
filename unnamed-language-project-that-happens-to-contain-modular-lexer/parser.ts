import {
    ExpressionNode,
    AssignmentNode,
    LetDeclarationNode,
    AdditionNode,
    SubtractionNode,
    MultiplicationNode,
    DivisionNode,
    RemainderNode,
    IntLiteralNode,
    CharLiteralNode,
    StringLiteralNode,
} from "./ast.ts";
import { Position, Span, Token } from "./lexer.ts";
import { TokenType } from "./tokentypes.ts";

export class ParserError extends Error {
    public constructor(message: string) {
        super(message);
        this.name = "ParserError";
    }

    public static fromPosition(pos: Position, message: string) {
        return new ParserError(`${message}, at ${pos}`);
    }

    public static fromSpan(span: Span, message: string) {
        return new ParserError(`${message}, at ${span}`);
    }
}

export class Parser {
    public index = 0;
    private saves: number[] = [];

    public constructor(public tokens: Token<TokenType>[]) {}

    public step() {
        if (this.index >= this.tokens.length)
            throw ParserError.fromPosition(
                this.tokens[this.tokens.length - 1].span.end,
                "unexpected end of file",
            );
        this.index++;
    }

    public current(): Token<TokenType> | null {
        if (this.index >= this.tokens.length) return null;
        return this.tokens[this.index];
    }

    public save() {
        this.saves.push(this.index);
    }

    public recover() {
        const fail = () => {
            throw new ParserError("cant recover unsaved parser state");
        };
        this.index = this.saves.pop() ?? fail();
    }
}

export const parse = (tokens: Token<TokenType>[]): ExpressionNode[] => {
    const self = new Parser(tokens);
    return parseExpressions(self);
};

export const parseExpressions = (self: Parser): ExpressionNode[] => {
    const expressions: ExpressionNode[] = [];
    while (self.index < self.tokens.length) {
        expressions.push(parseExpression(self));
    }
    return expressions;
};

export const parseExpression = (self: Parser): ExpressionNode => {
    if (self.current()!.type === TokenType.LetKeyword)
        return parseLetDeclaration(self);
    else return parseAssignment(self);
};

export const parseLetDeclaration = (self: Parser): ExpressionNode => {
    const begin = self.current()!.span.begin;
    self.step();
    if (self.current()?.type !== TokenType.Identifier)
        throw ParserError.fromSpan(self.current()!.span, "expected identifier");
    const { target, value } = parseAssignment(self) as AssignmentNode;
    return new LetDeclarationNode(target, value, begin);
};

export const parseFunctionDefinition = (self: Parser): ExpressionNode => {};

export const parseAssignment = (self: Parser): ExpressionNode => {
    const target = self.current()!;
    self.save();
    self.step();
    if (
        target.type === TokenType.Identifier &&
        self.current()?.type === TokenType.Equal
    ) {
        self.step();
        const value = parseExpression(self);
        return new AssignmentNode(target, value);
    } else {
        self.recover();
        return parseAdditionAndSubtraction(self);
    }
};

export const parseAdditionAndSubtraction = (self: Parser): ExpressionNode => {
    const left = parseMultiplicationDivisionAndRemainder(self);
    if (self.current()?.type === TokenType.Plus) {
        self.step();
        const right = parseAdditionAndSubtraction(self);
        return new AdditionNode(left, right);
    } else if (self.current()?.type === TokenType.Minus) {
        self.step();
        const right = parseAdditionAndSubtraction(self);
        return new SubtractionNode(left, right);
    } else return left;
};

export const parseMultiplicationDivisionAndRemainder = (
    self: Parser,
): ExpressionNode => {
    const left = parseValue(self);
    if (self.current()?.type === TokenType.Asterisk) {
        self.step();
        const right = parseMultiplicationDivisionAndRemainder(self);
        return new MultiplicationNode(left, right);
    } else if (self.current()?.type === TokenType.Slash) {
        self.step();
        const right = parseMultiplicationDivisionAndRemainder(self);
        return new DivisionNode(left, right);
    } else if (self.current()?.type === TokenType.Percentage) {
        self.step();
        const right = parseMultiplicationDivisionAndRemainder(self);
        return new RemainderNode(left, right);
    } else return left;
};

export const parseValue = (self: Parser): ExpressionNode => {
    if (self.current()?.type === TokenType.IntLiteral) {
        const value = self.current()!;
        self.step();
        return new IntLiteralNode(value);
    } else if (self.current()?.type === TokenType.HexLiteral) {
        const value = self.current()!;
        self.step();
        return new IntLiteralNode(value);
    } else if (self.current()?.type === TokenType.CharLiteral) {
        const value = self.current()!;
        self.step();
        return new CharLiteralNode(value);
    } else if (self.current()?.type === TokenType.StringLiteral) {
        const value = self.current()!;
        self.step();
        return new StringLiteralNode(value);
    } else if (self.current()?.type === TokenType.LParen) {
        self.step();
        const value = parseExpression(self);
        if (self.current()?.type !== TokenType.RParen)
            throw ParserError.fromPosition(
                self.current()!.span.begin,
                `expected ')'`,
            );
        self.step();
        return value;
    } else {
        throw ParserError.fromSpan(
            self.current()!.span,
            `unexpected token '${self.current()?.text}'`,
        );
    }
};
