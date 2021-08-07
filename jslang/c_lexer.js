
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
    INCLUDESTRING: 'INCLUDESTRING',
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
    constructor(type, text, value=null) {
        this.type = type;
        this.text = text;
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

    advance = (preserveAcc=false) => {
        if (!preserveAcc)
            this.accText = '';
        this.index++;
        this.currentChar = this.text.charAt(this.index) !== '' ? this.text.charAt(this.index) : null;
        this.accText += this.currentChar;
    }

    getAccText = (start=0, end=0) => this.accText.slice(start, end);

    lex = (text) => {
        this.text = text;
        this.index = -1;
        this.currentChar = null;
        const tokens = [];
        this.advance();
        while (this.currentChar !== null) {
            if (LETTERS.includes(this.currentChar)) {
                tokens.push(this.makeIdentifier());
            } else if (DIGITS.includes(this.currentChar)) {
                tokens.push(this.makeNumber());
            } else {
                switch (this.currentChar) {
                    case "'":
                        tokens.push(this.makeChar());
                        break;
                    case '"':
                        tokens.push(this.makeString());
                        break;
                    case '#':
                        tokens.push(new Token(TT.HASHTAG, '#'));
                        this.advance();
                        break;
                    case ' ':
                        tokens.push(new Token(TT.SPACE, ' '));
                        this.advance();
                        break;
                    case '\t':
                        tokens.push(new Token(TT.TAB, '\t'));
                        this.advance();
                        break;
                    case '\n':
                        tokens.push(new Token(TT.NEWLINE, '\n'));
                        this.advance();
                        break;
                    case ':':
                        tokens.push(new Token(TT.COLON, ':'));
                        this.advance();
                        break;
                    case ';':
                        tokens.push(new Token(TT.SEMICOLON, ';'));
                        this.advance();
                        break;
                    case ',':
                        tokens.push(new Token(TT.COMMA, ','));
                        this.advance();
                        break;
                    case '.':
                        tokens.push(new Token(TT.DOT, '.'));
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
                        if (this.afterIncludeStatement)
                            tokens.push(this.makeIncludeString());
                        else
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
                        tokens.push(new Token(TT.LPAREN, '('));
                        this.advance();
                        break;
                    case ')':
                        tokens.push(new Token(TT.RPAREN, ')'));
                        this.advance();
                        break;
                    case '[':
                        tokens.push(new Token(TT.LSQUARE, '['));
                        this.advance();
                        break;
                    case ']':
                        tokens.push(new Token(TT.RSQUARE, ']'));
                        this.advance();
                        break;
                    case '{':
                        tokens.push(new Token(TT.LBRACE, '{'));
                        this.advance();
                        break;
                    case '}':
                        tokens.push(new Token(TT.RBRACE, '}'));
                        this.advance();
                        break;
                    default:
                        throw new LexerError(`Illegal char '${this.currentChar}'`);
                }
            }
        }
        tokens.push(new Token(TT.EOF, ''));
        return tokens;
    }

    makeIdentifier = () => {
        let idString = '';
        while (this.currentChar !== null && (LETTERS + DIGITS).includes(this.currentChar)) {
            idString += this.currentChar;
            this.advance(true);
        }
        if (KEYWORDS.includes(idString)) {
            if (idString === 'include')
                this.afterIncludeStatement = true;
            return new Token(TT.KEYWORD, this.getAccText(0, -1), idString);
        } else
            return new Token(TT.IDENTIFIER, this.getAccText(0, -1), idString);
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
            this.advance(true);
        }
        if (dotCount === 0) 
            return new Token(TT.INT, this.getAccText(0, -1), parseInt(numString));
        else
            return new Token(TT.FLOAT, this.getAccText(0, -1), parseFloat(numString));
    }

    makeString = () => {
        let string = '';
        const escapeChars = {
            n: '\n',
            t: '\t'
        }
        this.advance(true);
        while (this.currentChar !== null && (this.currentChar !== '"')) {
            if (this.currentChar === '\\')
                string += escapeChars[this.currentChar] ? escapeChars[this.currentChar] : this.currentChar
            else
                string += this.currentChar;
            this.advance(true);
        }
        this.advance(true);
        return new Token(TT.STRING, this.getAccText(0, -1), string);
    }

    makeIncludeString = () => {
        let string = '';
        this.afterIncludeStatement = false;
        this.advance(true);
        while (this.currentChar !== null && this.currentChar !== '>') {
            string += this.currentChar;
            this.advance(true);
        }
        this.advance(true);
        return new Token(TT.INCLUDESTRING, this.getAccText(0, -1), string);
    }

    makeChar = () => {
        const charCode = this.currentChar.charCodeAt(0);
        let char = String.fromCharCode(charCode);
        this.advance(true);
        if (charCode < 0 || charCode > 255)
            char = '?';
        this.advance(true);
        if (this.currentChar !== "'")
            throw new LexerError("Expected `'` after 'CHAR'");
        this.advance(true);
        return new Token(TT.CHAR, this.getAccText(0, -1), char);
    }
    
    makePlusOrPlusEq = () => {
        let tokenType = TT.PLUS;
        this.advance(true);
        if (this.currentChar === '=') {
            tokenType = TT.PLUSEQ;
            this.advance(true);
        }
        return new Token(tokenType, this.getAccText(0, -1));
    }

    makeMinusOrMinusEq = () => {
        let tokenType = TT.MINUS;
        this.advance(true);
        if (this.currentChar === '=') {
            tokenType = TT.MINUSEQ;
            this.advance(true);
        }
        return new Token(tokenType, this.getAccText(0, -1));
    }

    makeMultiplyOrMultiplyEq = () => {
        let tokenType = TT.MULTIPLY;
        this.advance(true);
        if (this.currentChar === '=') {
            tokenType = TT.MULTIPLYEQ;
            this.advance(true);
        }
        return new Token(tokenType, this.getAccText(0, -1));
    }

    makeDivideOrDivideEq = () => {
        let tokenType = TT.DIVIDE;
        this.advance(true);
        if (this.currentChar === '=') {
            tokenType = TT.DIVIDEEQ;
            this.advance(true);
        }
        return new Token(tokenType, this.getAccText(0, -1));
    }

    makeEqualOrEE = () => {
        let tokenType = TT.EQUAL;
        this.advance(true);
        if (this.currentChar === '=') {
            tokenType = TT.EE;
            this.advance(true);
        }
        return new Token(tokenType, this.getAccText(0, -1));
    }

    makeNotOrNE = () => {
        let tokenType = TT.NOT;
        this.advance(true);
        if (this.currentChar === '=') {
            tokenType = TT.NE;
            this.advance(true);
        }
        return new Token(tokenType, this.getAccText(0, -1));
    }

    makeLtOrLte = () => {
        let tokenType = TT.LT;
        this.advance(true);
        if (this.currentChar === '=') {
            tokenType = TT.LTE;
            this.advance(true);
        }
        return new Token(tokenType, this.getAccText(0, -1));
    }
    
    makeGtOrGte = () => {
        let tokenType = TT.GT;
        this.advance(true);
        if (this.currentChar === '=') {
            tokenType = TT.GTE;
            this.advance(true);
        }
        return new Token(tokenType);
    }

    makeAndOrValueOf = () => {
        this.advance(true);
        if (this.currentChar !== '&') {
            return new Token(TT.VALUEOF, this.getAccText(0, -1));
        } else {
            this.advance(true);
            return new Token(TT.AND, this.getAccText(0, -1));
        }
    }

    makeOr = () => {
        this.advance(true);
        if (this.currentChar !== '|')
            throw new LexerError(`Expected '|' after '|'`)
        this.advance(true);
        return new Token(TT.AND, this.getAccText(0, -1));
    }

}
