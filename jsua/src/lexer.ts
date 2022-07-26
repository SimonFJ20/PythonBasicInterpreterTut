
export enum TokenType {
    Int                ,// = 'Int',
    Float              ,// = 'Float',
    String             ,// = 'String',
    Plus               ,// = 'Plus',
    Minus              ,// = 'Minus',
    Multiply           ,// = 'Multiply',
    Divide             ,// = 'Divide',
    PlusAssign         ,// = 'PlusAssign',
    MinusAssign        ,// = 'MinusAssign',
    MultiplyAssign     ,// = 'MultiplyAssign',
    DivideAssign       ,// = 'DivideAssign',
    EqualAssign        ,// = 'EqualAssign',
    Increment          ,// = 'Increment',
    Decrement          ,// = 'Decrement',
    LParen             ,// = 'LParen',
    RParen             ,// = 'RParen',
    LBrace             ,// = 'LBrace',
    RBrace             ,// = 'RBrace',
    LSquare            ,// = 'LSquare',
    RSquare            ,// = 'RSquare',
    EqualCompare       ,// = 'EqualCompare',
    NotEqual           ,// = 'NotEqual',
    LessThan           ,// = 'LessThan',
    GreaterThan        ,// = 'GreaterThan',
    LessThanOrEqual    ,// = 'LessThanOrEqual',
    GreaterThanOrEqual ,// = 'GreaterThanOrEqual',
    Identifier         ,// = 'Identifier',
    Keyword            ,// = 'Keyword',
    Comma              ,// = 'Comma',
    Colon              ,// = 'Colon',
    Newline            ,// = 'Newline',
    EndOfFile          ,// = 'EndOfFile',
}

export const Keywords: string[] = [
    'int',
    'float',
    'string',
    'bool',
    'func',
    'if',
    'while',
    'for',
    'continue',
    'break',
    'return',
    'require',
]

export enum KeywordTypes {
    Int         = 0,
    Float       = 1,
    String      = 2,
    Bool        = 3,
    Func        = 4,
    If          = 5,
    While       = 6,
    For         = 7,
    Continue    = 8,
    Break       = 9,
    Return      = 10,
    Require     = 11,
}

export class Token {
    constructor (public type: TokenType, public value?: any) {}
    public matches = (token?: Token) => this.type === token?.type && this.value === token.value;
}

export class Consts {
    public static digits = '0123456789';
    public static lowerCaseLetters = 'abcdefghijklmnopqrstuvwxyz';
    public static upperCaseLetters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    public static letters = Consts.lowerCaseLetters + Consts.upperCaseLetters;
    public static lettersDigits = Consts.digits + Consts.letters;
    public static escapedChars: {[key: string]: string} = {
        'n': '\n',
        't': '\t',
    };
}

export class Lexer {
    private text: string = '';
    private textIndex: number = 0;
    private currentChar: string | null = null;

    private advance = () => {
        this.textIndex++;
        const c = this.text.charAt(this.textIndex);
        this.currentChar = c !== '' ? c : null;
    }

    private makeNumber = (): Token => {
        let value = this.currentChar!;
        this.advance();

        let decimalPoints = 0;
        while (this.currentChar !== null && (Consts.digits + '.').includes(this.currentChar)) {
            if (this.currentChar === '.')
                decimalPoints++;
            if (decimalPoints > 1)
                break;
            value += this.currentChar;
            this.advance();
        }

        if (decimalPoints)
            return new Token(TokenType.Float, parseFloat(value));
        else
            return new Token(TokenType.Int, parseInt(value));
    }

    private makeIdentifierOrKeyword = (): Token => {
        let value = this.currentChar!;
        this.advance();

        while (this.currentChar !== null && Consts.lettersDigits.includes(this.currentChar!)) {
            value += this.currentChar;
            this.advance();
        }

        if (Keywords.includes(value))
            return new Token(TokenType.Keyword, value);
        else
            return new Token(TokenType.Identifier, value);
    }

    private makeString = (): Token => {
        let value = '';
        const stringChar = this.currentChar;
        this.advance();

        let escaped = false;
        while (this.currentChar !== null && (this.currentChar !== stringChar || escaped)) {
            if (escaped) {
                const escapedChar = Consts.escapedChars[this.currentChar];
                value += escapedChar ? escapedChar : this.currentChar;
                escaped = false;
            } else {
                if (this.currentChar == '\\')
                    escaped = true;
                else
                    value += this.currentChar;
            }
            this.advance();
        }

        if (this.currentChar === null)
            throw new Error(`Expected '${stringChar}' got NULL`);
        else if (this.currentChar !== stringChar)
            throw new Error(`Expected '${stringChar}' got '${this.currentChar}'`);
        
        this.advance();
        return new Token(TokenType.String, value)
    }

    private makePlus = () => {
        this.advance();
        if (this.currentChar === '=') {
            this.advance();
            return new Token(TokenType.PlusAssign);
        } else if (this.currentChar === '+') {
            this.advance();
            return new Token(TokenType.Increment);
        }
        return new Token(TokenType.Plus);
    }

    private makeMinus = () => {
        this.advance();
        if (this.currentChar === '=') {
            this.advance();
            return new Token(TokenType.MinusAssign);
        } else if (this.currentChar === '-') {
            this.advance();
            return new Token(TokenType.Decrement);
        }
        return new Token(TokenType.Minus);
    }

    private makeMultiply = () => {
        this.advance();
        if (this.currentChar === '=') {
            this.advance();
            return new Token(TokenType.MultiplyAssign);
        }
        return new Token(TokenType.Multiply);
    }

    private makeDivide = () => {
        this.advance();
        if (this.currentChar === '=') {
            this.advance();
            return new Token(TokenType.DivideAssign);
        }
        return new Token(TokenType.Divide);
    }

    private makeNot = (): Token => {
        this.advance();
        if (this.currentChar === '=') {
            this.advance();
            return new Token(TokenType.NotEqual);
        }
        return new Token(TokenType.NotEqual);
    }

    private makeEqual = (): Token => {
        this.advance();
        if (this.currentChar === '=') {
            this.advance();
            return new Token(TokenType.EqualCompare);
        }
        return new Token(TokenType.EqualAssign);
    }

    private makeLessThan = (): Token => {
        this.advance();
        if (this.currentChar === '=') {
            this.advance();
            return new Token(TokenType.LessThanOrEqual);
        }
        return new Token(TokenType.LessThan);
    }

    private makeGreaterThan = (): Token => {
        this.advance();
        if (this.currentChar === '=') {
            this.advance();
            return new Token(TokenType.GreaterThanOrEqual);
        }
        return new Token(TokenType.GreaterThan);
    }

    private addTokenAndAdvance = (tokens: Token[], type: TokenType) => {
        tokens.push(new Token(type));
        this.advance();
    }

    public lex = (text: string): Token[] => {
        this.text = text;
        this.textIndex = -1;
        this.advance();

        const tokens: Token[] = [];
        while (this.currentChar !== null) {
            if (Consts.digits.includes(this.currentChar)) {
                tokens.push(this.makeNumber());
            } else if (Consts.letters.includes(this.currentChar)) {
                tokens.push(this.makeIdentifierOrKeyword());
            } else {
                switch (this.currentChar) {
                    case '"':
                    case "'": tokens.push(this.makeString()); break;
                    case ' ':
                    case '\t': this.advance(); break;
                    case ';':
                    case '\n': this.addTokenAndAdvance(tokens, TokenType.Newline); break;
                    case '+': tokens.push(this.makePlus()); break;
                    case '-': tokens.push(this.makeMinus()); break;
                    case '*': tokens.push(this.makeMultiply()); break;
                    case '/': tokens.push(this.makeDivide()); break;
                    case '(': this.addTokenAndAdvance(tokens, TokenType.LParen); break;
                    case ')': this.addTokenAndAdvance(tokens, TokenType.RParen); break;
                    case '{': this.addTokenAndAdvance(tokens, TokenType.LBrace); break;
                    case '}': this.addTokenAndAdvance(tokens, TokenType.RBrace); break;
                    case '[': this.addTokenAndAdvance(tokens, TokenType.LSquare); break;
                    case ']': this.addTokenAndAdvance(tokens, TokenType.RSquare); break;
                    case '=': tokens.push(this.makeNot()); break;
                    case '!': tokens.push(this.makeEqual()); break;
                    case '<': tokens.push(this.makeLessThan()); break;
                    case '>': tokens.push(this.makeGreaterThan()); break;
                    case ',': this.addTokenAndAdvance(tokens, TokenType.Comma); break;
                    case ':': this.addTokenAndAdvance(tokens, TokenType.Colon); break;
                    default: throw new Error(`Illegal Character: '${this.currentChar}'`);
                }
            }
        }
        tokens.push(new Token(TokenType.EndOfFile));
        return tokens;
    }

}
