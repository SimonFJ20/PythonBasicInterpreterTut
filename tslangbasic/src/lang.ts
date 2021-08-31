
type char = string;

const DIGITS = '0123456789';
const LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';

class Position {
    constructor (
        public index: number, 
        public linenumber: number, 
        public column: number, 
        public filename: string, 
        public filetext: string
    ) {}

    public advance = (currChar?: char) => {
        this.index++;
        this.column++;

        if (currChar === '\n') {
            this.linenumber++;
            this.column = 0;
        }

        return this;
    }

    public copy = () => new Position(
        this.index, 
        this.linenumber, 
        this.column, 
        this.filename, 
        this.filetext
    );
}

class LangError {
    protected getArrowString = (text: string, pStart: Position, pEnd: Position) => {
        let result = '';
        let indexStart = Math.max(text.lastIndexOf('\n', pStart.index), 0);
        let indexEnd = text.indexOf('\n', indexStart + 1) >= 0 ? text.indexOf('\n', indexStart + 1) : text.length;
        
        const lineCount = pEnd.linenumber - pStart.linenumber + 1;
        for (let i = 0; i < lineCount; i++) {
            const line = text.slice(indexStart, indexEnd);
            const columnStart = i === 0 ? pStart.column : 0;
            const columnEnd = i === lineCount - 1 ? pEnd.column : line.length - 1;
    
            result += `${line}\n`;
            result += `${' '.repeat(columnStart)}${'^'.repeat(columnEnd - columnStart)}`;
    
            indexStart = indexEnd;
            indexEnd = text.indexOf('\n', indexStart + 1) >= 0 ? text.indexOf('\n', indexStart + 1) : text.length;
        }
    
        return result.replace(/\t/g, '');
    }

    constructor (
        public pStart: Position,
        public pEnd: Position,
        public errorName: string,
        public details: string
    ) {}

    public toString = () => {
        let result = `${this.errorName}: ${this.details}\n`;
        result += `On line ${this.pStart.linenumber + 1}, in "${this.pStart.filename}"`;
        result += `\n\n${this.getArrowString(this.pStart.filetext, this.pStart, this.pEnd)}`;
        return result;
    }
}

class IllegalCharError extends LangError {
    constructor (pStart: Position, pEnd: Position, details: string) {
        super(pStart, pEnd, 'Illegal Character', details);
    }
}

class ExpectedCharError extends LangError {
    constructor (pStart: Position, pEnd: Position, details: string) {
        super(pStart, pEnd, 'Expected Character', details);
    }
}

class InvalidSyntaxError extends LangError {
    constructor (pStart: Position, pEnd: Position, details: string) {
        super(pStart, pEnd, 'Invalid Syntax', details);
    }
}

class RTError extends LangError {
    private generateTraceback = () => {
        let result = '';
        let position = this.pStart;
        let context = this.context;
        while (context) {
            // result = ` File ${position.filename}, line ${position.linenumber + 1}, in ${context.displayName}\n` + result;
            // position = context.parentEntryPos;
            // context = context.parent;
        }
        return `Traceback (most recent call last):\n${result}`;
    }
    
    constructor (pStart: Position, pEnd: Position, details: string, private context: Context) {
        super(pStart, pEnd, 'Runtime Error', details);
    }

    public toString = () => {
        let result = this.generateTraceback();
        result += `${this.errorName}: ${this.details}\n`;
        result += `On line ${this.pStart.linenumber + 1}, in "${this.pStart.filename}"`;
        result += `\n\n${this.getArrowString(this.pStart.filetext, this.pStart, this.pEnd)}`;
        return result;
    }
}

enum TT {
    int,
    float,
    string,
    identifier,
    keyword,
    plus,
    minus,
    multiply,
    divide,
    power,
    equals,
    lParen,
    rParen,
    lSquare,
    rSquare,
    ee,
    ne,
    lt,
    gt,
    lte,
    gte,
    comma,
    arrow,
    newline,
    eof,
}

const Keywords = [
    'var',
    'and',
    'or',
    'not',
    'if',
    'elseif',
    'else',
    'for',
    'to',
    'step',
    'while',
    'function',
    'then',
    'do',
    'end',
    'return',
    'continue',
    'break',
]

class Token {
    public pStart?: Position;
    public pEnd?: Position;

    constructor(
        public type: TT,
        public value?: any,
        pStart?: Position,
        pEnd?: Position
    ) {
        if (pStart) {
            this.pStart = pStart.copy();
            this.pEnd = pStart.copy();
            this.pEnd.advance();
        }

        if (pEnd) {
            this.pEnd = pEnd.copy();
        }
    }

    public matches = (type: TT, value: any) => this.type === type && this.value === this.value;
    public toString = () => this.value ? `${this.type}${this.value}` : `${this.type}`;
}

export class Lexer {
    public position: Position;
    public currChar?: char;

    private advance = () => {
        this.position.advance(this.currChar);
        this.currChar = this.position.index < this.text.length ? this.text.charAt(this.position.index) : undefined;
    }

    constructor (
        public filename: string,
        public text: string
    ) {
        this.position = new Position(-1, 0, -1, filename, text);
        this.currChar = undefined;
        this.advance();
    }

    private makeNumber = (): Token => {
        let numberString = '';
        let dotCount = 0;
        const pStart = this.position.copy();
        
        while (this.currChar !== undefined && '0123456789.'.includes(this.currChar)) {
            if (this.currChar === '.')
                if (dotCount++ === 1)
                    break;
            numberString += this.currChar;
            this.advance()
        }

        if (dotCount)
            return new Token(TT.float, parseFloat(numberString), pStart, this.position);
        else
            return new Token(TT.int, parseInt(numberString), pStart, this.position);
    }

    private makeString = (): Token => {
        let stringValue = '';
        const pStart = this.position.copy();
        let escapeChar = false;
        this.advance();

        const escapeCharacters: {[key: string]: string} = {'n': '\n', 't': '\t'};

        while (this.currChar !== undefined && (this.currChar !== '"' || escapeChar)) {
            if (escapeChar) {
                stringValue += escapeCharacters[this.currChar] || this.currChar;
                escapeChar = false;
            } else
                if (this.currChar === '\\')
                    escapeChar = true;
                else
                    stringValue += this.currChar;
            this.advance();
        }

        this.advance();
        return new Token(TT.string, stringValue, pStart, this.position);
    }

    private makeIdentifier = (): Token => {
        let idString = '';
        const pStart = this.position.copy();

        while (this.currChar !== undefined && (LETTERS + DIGITS + '_').includes(this.currChar)) {
            idString += this.currChar;
            this.advance();
        }

        const tokenType = Keywords.includes(idString) ? TT.keyword: TT.identifier;
        return new Token(tokenType, idString, pStart, this.position);
    }

    private makeNotEquals = (): [Token?, ExpectedCharError?] => {
        const pStart = this.position.copy();
        this.advance();

        if (this.currChar === '=') {
            this.advance();
            return [new Token(TT.ne, undefined, pStart, this.position), undefined];
        }

        this.advance();
        return [undefined, new ExpectedCharError(pStart, this.position, `'=' (after '!')`)];
    }

    public lex = (): [Token[]?, LangError?] => {
        const tokens: Token[] = [];

        while (this.currChar !== undefined) {
            if (DIGITS.includes(this.currChar)) {

            } else if (LETTERS.includes(this.currChar)) {

            } else {
                switch (this.currChar) {
                case ' ':
                case '\t':
                    this.advance();
                    break;
                case '#':
                    break;
                case ';':
                case '\n':
                    break;
                case '"':
                    break;
                case '+':
                    break;
                case '-':
                    break;
                case '*':
                    break;
                case '/':
                    break;
                case '^':
                    break;
                case '(':
                    break;
                case ')':
                    break;
                case '[':
                    break;
                case ']':
                    break;
                case '!':
                    break;
                case '=':
                    break;
                case '<':
                    break;
                case '>':
                    break;
                case ',':
                    break;
                default:
                    const pStart = this.position.copy();
                    const char = this.currChar;
                    this.advance();
                    return [[], new IllegalCharError(pStart, this.position, `'${char}'`)];
                }
            }
        }
        tokens.push(new Token(TT.eof, undefined, this.position));
        return [tokens, undefined];
    }

}

class Node {

}

export class Parser {

    public parse = () => {

    }

}

class Context {

}
