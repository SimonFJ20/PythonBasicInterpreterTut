
export class Position {
    public constructor (
        public row: number,
        public column: number,
    ) {}

    public copy() {
        return new Position(this.row, this.column);
    }

    public toString(): string {
        return `${this.row}:${this.column}`
    }
}

export class Span {
    public constructor (
        public begin: Position,
        public end: Position,
    ) {}

    public toString(): string {
        return `${this.begin} to ${this.end}`
    }
}

export class Token<TokenType> {
    public constructor (
        public type: TokenType,
        public span: Span,
        public text: string,
        public value: string = text,
    ) {}
}

export class LexerError extends Error {
    public constructor (message: string) {
        super (message);
        this.name = 'LexerError';
    }

    public static fromPosition(pos: Position, message: string) {
        return new LexerError(`${message}, at ${pos}`)
    }

    public static fromSpan(span: Span, message: string) {
        return new LexerError(`${message}, at ${span}`)
    }
}

export class Lexer {
    public index = 0;
    public pos = new Position(1, 1,);
    private _prevPos: Position | null = null;

    public constructor (
        public text: string,
    ) {}

    public step() {
        if (this.index >= this.text.length)
            throw LexerError.fromPosition(this.pos, 'unexpected end of file');
        this.index++;
        this._prevPos = this.pos.copy();
        if (this.text[this.index - 1] === '\n') {
            this.pos.row++;
            this.pos.column = 1;
        } else {
            this.pos.column++;
        }
    }

    public prevPos(): Position {
        if (!this._prevPos)
            throw LexerError.fromPosition(this.pos, 'no previus position');
        return this._prevPos;
    }
}

export type LexerRule<TokenType> = {
    pattern: RegExp,
    handler: (self: Lexer) => Token<TokenType> | null,
};

export const tokenize = <TokenType>(text: string, rules: LexerRule<TokenType>[]): Token<TokenType>[] => {
    const self = new Lexer(text);
    const tokens: Token<TokenType>[] = [];
    while (self.index < self.text.length) {
        const indexBefore = self.index;
        const rule = rules.find((rule) => rule.pattern.test(self.text.slice(self.index)));
        if (!rule)
            throw LexerError.fromPosition(
                self.pos,
                `unhandled character '${self.text.slice(
                    self.index,
                    self.index + Math.min(10, self.text.length - self.index, self.text.slice(self.index).indexOf('\n'))
                )}'`
            );
        const maybeToken = rule.handler(self);
        if (maybeToken)
            tokens.push(maybeToken);
        if (self.index === indexBefore)
            throw LexerError.fromSpan(
                new Span(self.prevPos(), self.pos),
                `rule with pattern '${rule.pattern.toString()}' doesn't step lexer forward`
            );
    }
    return tokens;
}



export const hexRule = <TokenType>(tokenType: TokenType): LexerRule<TokenType> => {
    return {
        pattern: /^0x/,
        handler: (self) => {
            const begin = self.pos.copy();
            let text = self.text[self.index];
            self.step();
            text += self.text[self.index];
            self.step();
            while (/^[0-9a-fA-F]/.test(self.text[self.index])) {
                text += self.text[self.index];
                self.step();
            }
            const end = self.prevPos().copy();
            return new Token(tokenType, new Span(begin, end), text);
        }, 
    };
}

export const intRule = <TokenType>(tokenType: TokenType): LexerRule<TokenType> => {
    return {
        pattern: /^[0-9]/,
        handler: (self) => {
            const begin = self.pos.copy();
            let text = '';
            while (/[0-9]/.test(self.text[self.index])) {
                text += self.text[self.index];
                self.step();
            }
            const end = self.prevPos().copy();
            return new Token(tokenType, new Span(begin, end), text);
        }, 
    };
}

export const identifierRule = <TokenType>(tokenType: TokenType): LexerRule<TokenType> => {
    return {
        pattern: /^[a-zA-Z_]/,
        handler: (self) => {
            const begin = self.pos.copy();
            let text = '';
            while (/[a-zA-Z_]/.test(self.text[self.index])) {
                text += self.text[self.index];
                self.step();
            }
            const end = self.prevPos().copy();
            return new Token(tokenType, new Span(begin, end), text);
        }
    };
}

export const ignorePatternRule = <TokenType>(pattern: RegExp): LexerRule<TokenType> => {
    return {
        pattern,
        handler: (self) => {
            while (pattern.test(self.text[self.index]))
                self.step();
            return null;
        },
    };
}

export const ignoreSingleLineWhitespaceRule = <TokenType>(): LexerRule<TokenType> => {
    return {
        pattern: /^[ \t]/,
        handler: (self) => {
            while (/[ \t]/.test(self.text[self.index]))
                self.step();
            return null;
        },
    };
}

export const singleLineWhitespaceRule = <TokenType>(tokenType: TokenType): LexerRule<TokenType> => {
    return {
        pattern: /^[ \t]/,
        handler: (self) => {
            const begin = self.pos.copy();
            let text = '';
            while (/[ \t]/.test(self.text[self.index])) {
                text += self.text[self.index];
                self.step();
            }
            const end = self.prevPos().copy();
            return new Token(tokenType, new Span(begin, end), text);
        },
    };
}

export const ignoreSingleLineComment = <TokenType>(): LexerRule<TokenType> => {
    return {
        pattern: /^\/\//,
        handler: (self) => {
            while (self.index < self.text.length && self.text[self.index] !== '\n')
                self.step();
            return null;
        }
    };
}

export const ignoreMultiLineComment = <TokenType>(): LexerRule<TokenType> => {
    return {
        pattern: /^\/\*/,
        handler: (self) => {
            while (self.index < self.text.length && (self.text[self.index - 1] !== '*' || self.text[self.index] !== '/'))
                self.step();
            self.step();
            return null;
        }
    };
} 

export const makeLiteralChar = (self: Lexer): string => {
    const char = self.text[self.index];
    self.step();
    if (char !== '\\') {
        return char;
    } else {
        const identifier = self.text[self.index];
        self.step();
        if (identifier === '0') {
            let value = self.text[self.index];
            self.step();
            for (let i = 0; i < 3 && /[0-7]/.test(self.text[self.index]); i++)
                value += self.text[self.index];
            return String.fromCharCode(parseInt(value, 8));
        } else if (identifier === 'x') {
            let value = '';
            self.step();
            for (let i = 0; i < 2 && /[0-9a-zA-Z]/.test(self.text[self.index]); i++)
                value += self.text[self.index];
            return String.fromCharCode(parseInt(value, 16));
        } else if (/[1-9]/.test(identifier)) {
            let value = self.text[self.index];
            self.step();
            for (let i = 0; i < 3 && /[0-9]/.test(self.text[self.index]); i++)
                value += self.text[self.index];
            return String.fromCharCode(parseInt(value, 10));
        } else {
            switch (identifier) {
                case 'b': return '\b';
                case 'f': return '\f';
                case 'n': return '\n';
                case 'r': return '\r';
                case 't': return '\t';
                case 'v': return '\v';
                default: return identifier;
            }
        }
        
    }
}

export const charLiteralRule = <TokenType>(tokenType: TokenType): LexerRule<TokenType> => {
    return {
        pattern: /^'/,
        handler: (self) => {
            const begin = self.pos.copy();
            let text = self.text[self.index];
            self.step();
            if (self.text[self.index] === '\'')
                throw LexerError.fromSpan(new Span(begin, self.pos), 'char literal cannot be empty');
            const value = makeLiteralChar(self);
            text += value;
            text += self.text[self.index];
            if (self.text[self.index] !== '\'')
                throw LexerError.fromSpan(new Span(begin, self.pos), 'char literal can only contain 1 char');
            self.step();
            const end = self.prevPos().copy();
            return new Token(tokenType, new Span(begin, end), text, value);
        },
    };
}

export const stringLiteralRule = <TokenType>(tokenType: TokenType): LexerRule<TokenType> => {
    return {
        pattern: /^"/,
        handler: (self) => {
            const begin = self.pos.copy();
            let text = self.text[self.index];
            let value = '';
            self.step();
            while (self.index < self.text.length && self.text[self.index] !== '\"') {
                const literalChar = makeLiteralChar(self);
                value += literalChar;
                text += literalChar;
            }
            text += self.text[self.index];
            if (self.text[self.index] !== '\"')
                throw LexerError.fromSpan(new Span(begin, self.pos), 'unterminated string literal');
            self.step();
            const end = self.prevPos().copy();
            return new Token(tokenType, new Span(begin, end), text, value);
        },
    };
}

export const charPatternRule = <TokenType>(tokenType: TokenType, pattern: string): LexerRule<TokenType> => {
    const safePattern = pattern.replaceAll(/([\b\n\f\r\t\v\(\)\{\}\[\]\.\\\^\-\?\+\|\*])/g, '\\$1');
    return {
        pattern: new RegExp(`^${safePattern}`),
        handler: (self) => {
            const begin = self.pos.copy();
            pattern.split('').forEach(() => self.step());
            const end = self.prevPos().copy();
            return new Token(tokenType, new Span(begin, end), pattern);
        },
    };
}
