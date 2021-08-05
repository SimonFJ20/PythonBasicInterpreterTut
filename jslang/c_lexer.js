
const DIGITS = '0123456789';
const LETTERS = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';


class LexerError extends Error {
    constructor(msg) {
        super(msg);
        this.name = 'LexerError';
    }
}


const TT = {
    HASHTAG: 'HASHTAG',
    INT: 'INT',
    FLOAT: 'FLOAT',
    CHAR: 'CHAR',
    STRING: 'STRING',
    IDENTIFIER: 'IDENTIFIER',
    KEYWORD: 'KEYWORD',
    PLUS: 'PLUS',
    MINUS: 'MINUS',
    MULTIPLY: 'MULTIPLY',
    DIVIDE: 'DIVIDE',
    PLUSEQ: 'PLUSEQ',
    MINUSEQ: 'MINUSEQ',
    MULTIPLYEQ: 'MULTIPLYEQ',
    DIVIDEEQ: 'DIVIDEEQ',
    EQUAL: 'EQUAL',
    LPAREN: 'LPAREN',
    RPAREN: 'RPAREN',
    LSQUARE: 'LSQUARE',
    RSQUARE: 'RSQUARE',
    LBRACE: 'LBRACE',
    RBRACE: 'RBRACE',
    EE: 'EE',
    NE: 'NE',
    LT: 'LT',
    GT: 'GT',
    LTE: 'LTE',
    GTE: 'GTE',
    AND: 'AND',
    OR: 'OR',
    NOT: 'NOT',
    COMMA: 'COMMA',
    COLON: 'COLON',
    SEMICOLON: 'SEMICOLON',
    DOT: 'DOT',
    VALUEOF: 'VALUEOF',
    SPACE: 'SPACE',
    TAB: 'TAB',
    NEWLINE: 'NEWLINE',
    EOF: 'EOF',
};

const KEYWORDS = [
    'include',
    'define',
    'void',
    'int',
    'float',
    'double',
    'char',
    'if',
    'else',
    'for',
    'while',
    'do',
    'break',
    'continue',
    'return',
];

class Token {
    constructor(type, value=null) {
        this.type = type;
        this.value = value;
    }
    toString = () => {
        if (this.value)
            return `[${this.type}:${this.value}]`;
        else
            return `[${this.type}]`;
    }
}

class Lexer {
    constructor() {
        this.text = null;
        this.index = -1;
        this.currentChar = null;
    }

    advance = () => {
        this.index++;
        this.currentChar = this.text.charAt(this.index) !== '' ? this.text.charAt(this.index) : null;
    }

    lex = (text) => {
        const tokens = [];
        this.text = text;
        this.advance();
        while (this.currentChar !== null) {
            if (LETTERS.includes(this.currentChar)) {
                this.makeIdentifier();
            } else if (DIGITS.includes(this.currentChar)) {
                this.makeNumber();
            } else {
                switch (this.currentChar) {
                    case "'":
                        tokens.push(this.makeChar());
                        break;
                    case '"':
                        tokens.push(this.makeString());
                        break;
                    case '#':
                        tokens.push(new Token(TT.HASHTAG));
                        this.advance();
                        break;
                    case ' ':
                        tokens.push(new Token(TT.SPACE));
                        this.advance();
                        break;
                    case '\t':
                        tokens.push(new Token(TT.TAB));
                        this.advance();
                        break;
                    case '\n':
                        tokens.push(new Token(TT.NEWLINE));
                        this.advance();
                        break;
                    case ':':
                        tokens.push(new Token(TT.COLON));
                        this.advance();
                        break;
                    case ';':
                        tokens.push(new Token(TT.SEMICOLON));
                        this.advance();
                        break;
                    case ',':
                        tokens.push(new Token(TT.COMMA));
                        this.advance();
                        break;
                    case '.':
                        tokens.push(new Token(TT.DOT));
                        this.advance();
                        break;
                    case '+':
                        tokens.push(this.makePlusOrPlusEq());
                        break;
                    case '-':
                        tokens.push(this.makeMinusOrMinusEq());
                        break;
                    case '*':
                        tokens.push(this.makeMultiplyOrMultiplyEq());
                        break;
                    case '/':
                        tokens.push(this.makeDivideOrDivideEq());
                        break;
                    case '=':
                        tokens.push(this.makeEqualOrEE());
                        break;
                    case '!':
                        tokens.push(this.makeNotOrNE());
                        break;
                    case '<':
                        tokens.push(this.makeLtOrLte());
                        break;
                    case '>':
                        tokens.push(this.makeGtOrGte());
                        break;
                    case '&':
                        tokens.push(this.makeAndOrValueOf());
                        break;
                    case '|':
                        tokens.push(this.makeOr());
                        break;
                    case '(':
                        tokens.push(new Token(TT.LPAREN));
                        this.advance();
                        break;
                    case ')':
                        tokens.push(new Token(TT.RPAREN));
                        this.advance();
                        break;
                    case '[':
                        tokens.push(new Token(TT.LSQUARE));
                        this.advance();
                        break;
                    case ']':
                        tokens.push(new Token(TT.RSQUARE));
                        this.advance();
                        break;
                    case '{':
                        tokens.push(new Token(TT.LBRACE));
                        this.advance();
                        break;
                    case '}':
                        tokens.push(new Token(TT.RBRACE));
                        this.advance();
                        break;
                    default:
                        throw new LexerError(`Illegal char '${this.currentChar}'`);
                }
            }
        }
        return tokens;
    }

    makeIdentifier = () => {
        let idString = '';
        while (this.currentChar !== null && (LETTERS + DIGITS).includes(this.currentChar)) {
            idString += this.currentChar;
            this.advance();
        }
        if (idString in KEYWORDS)
            return new Token(TT.KEYWORD, idString);
        else
            return new Token(TT.IDENTIFIER, idString);
    }

    makeNumber = () => {
        let numString = '';
        let dotCount = 0;
        while (this.currentChar !== null && (DIGITS + '.').includes(this.currentChar)) {
            if (this.currentChar === '.') {
                if (dotCount === 1)
                    break;
                dotCount++;
            }
            numString += this.currentChar;
            this.advance();
        }
        if (dotCount === 0) 
            return new Token(TT.INT, parseInt(numString));
        else
            return new Token(TT.FLOAT, parseFloat(numString));
    }

    makeString = () => {
        let string = '';
        let escaped = false;
        const escapeChars = {
            n: '\n',
            t: '\t'
        }
        this.advance();
        while (this.currentChar !== null && (this.currentChar !== '"' || escaped)) {
            if (escaped) {
                string += escapeChars[this.currentChar] ? escapeChars[this.currentChar] : this.currentChar
            } else {
                if (this.currentChar === '\\')
                    escaped = true;
                else
                    string += this.currentChar;
            }
            escaped = false;
            this.advance();
        }
        this.advance();
        return new Token(TT.STRING, string);
    }

    makeChar = () => {
        const charCode = this.currentChar.charCodeAt(0);
        let char = String.fromCharCode(charCode);
        this.advance();
        if (charCode < 0 || charCode > 255)
            char = '?';
        this.advance();
        if (this.currentChar !== "'")
            throw new LexerError("Expected `'` after 'CHAR'");
        this.advance();
        return new Token(TT.CHAR, char);
    }
    
    makePlusOrPlusEq = () => {
        let tokenType = TT.PLUS;
        this.advance();
        if (this.currentChar === '=') {
            tokenType = TT.PLUSEQ;
            this.advance();
        }
        return new Token(tokenType);
    }

    makeMinusOrMinusEq = () => {
        let tokenType = TT.MINUS;
        this.advance();
        if (this.currentChar === '=') {
            tokenType = TT.MINUSEQ;
            this.advance();
        }
        return new Token(tokenType);
    }

    makeMultiplyOrMultiplyEq = () => {
        let tokenType = TT.MULTIPLY;
        this.advance();
        if (this.currentChar === '=') {
            tokenType = TT.MULTIPLYEQ;
            this.advance();
        }
        return new Token(tokenType);
    }

    makeDivideOrDivideEq = () => {
        let tokenType = TT.DIVIDE;
        this.advance();
        if (this.currentChar === '=') {
            tokenType = TT.DIVIDEEQ;
            this.advance();
        }
        return new Token(tokenType);
    }

    makeEqualOrEE = () => {
        let tokenType = TT.EQUAL;
        this.advance();
        if (this.currentChar === '=') {
            tokenType = TT.EE;
            this.advance();
        }
        return new Token(tokenType);
    }

    makeNotOrNE = () => {
        let tokenType = TT.NOT;
        this.advance();
        if (this.currentChar === '=') {
            tokenType = TT.NE;
            this.advance();
        }
        return new Token(tokenType);
    }

    makeLtOrLte = () => {
        let tokenType = TT.LT;
        this.advance();
        if (this.currentChar === '=') {
            tokenType = TT.LTE;
            this.advance();
        }
        return new Token(tokenType);
    }
    
    makeGtOrGte = () => {
        let tokenType = TT.GT;
        this.advance();
        if (this.currentChar === '=') {
            tokenType = TT.GTE;
            this.advance();
        }
        return new Token(tokenType);
    }

    makeAndOrValueOf = () => {
        this.advance();
        if (this.currentChar !== '&') {
            return new Token(TT.VALUEOF);
        } else {
            this.advance();
            return new Token(TT.AND);
        }
    }

    makeOr = () => {
        this.advance();
        if (this.currentChar !== '|')
            throw new LexerError(`Expected '|' after '|'`)
        this.advance();
        return new Token(TT.AND);
    }

}
