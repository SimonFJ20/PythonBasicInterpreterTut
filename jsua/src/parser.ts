import { Keywords, KeywordTypes, Token, TokenType } from "./lexer";

class InvalidSyntaxError {
    public name: string = 'Invalid Syntax'
    constructor(public details: string) {

    }
    public toString = () => `\n${this.name}: ${this.details}\n`;
}

class ParseNode {

}

class ListNode extends ParseNode {
    constructor (public nodes: ParseNode[]) { 
        super();
    }
}

class ReturnNode extends ParseNode {
    constructor (public node?: ParseNode) {
        super();
    }
}

class ContinueNode extends ParseNode {
    constructor () {
        super();
    }
}

class BreakNode extends ParseNode {
    constructor () {
        super();
    }
}

class ParseResult {
    public node?: ParseNode = undefined;
    public error?: InvalidSyntaxError = undefined;
    public lastRegisteredAdvanceCount: number = 0;
    public advanceCount: number = 0;
    public toReverseCount: number = 0;

    public registerAdvance = () => {
        this.lastRegisteredAdvanceCount = 1;
        this.advanceCount++;
    }

    public register = (result: ParseResult) => {
        this.lastRegisteredAdvanceCount = this.advanceCount;
        this.advanceCount += result.advanceCount;
        if (result.error)
            this.error = result.error;
        return result.node;
    }

    public tryRegister = (result: ParseResult) => {
        if (result.error) {
            this.toReverseCount = result.advanceCount;
            return undefined;
        }
        return this.register(result);
    }

    public success = (node: ParseNode) => {
        this.node = node;
        return this;
    }

    public failure = (error: InvalidSyntaxError) => {
        if (!this.error || this.lastRegisteredAdvanceCount === 0)
            this.error = error;
        return this;
    }
}

export class Parser {
    private tokens: Token[] = [];
    private tokenIndex: number = 0;
    private currentToken: Token | null = null;

    private updateCurrentToken = () => {
        if (this.tokenIndex >= 0 && this.tokenIndex < this.tokens.length)
            this.currentToken = this.tokens[this.tokenIndex];
    }

    private advance = () => {
        this.tokenIndex++;
        this.updateCurrentToken();
        return this.currentToken;
    }

    private reverse = (amount: number = 1) => {
        this.tokenIndex -= amount;
        this.updateCurrentToken();
        return this.currentToken;
    }

    private makeStatement = (): ParseResult => {
        const result = new ParseResult();

        // if (this.currentToken?.type === TokenType.Keyword 
        // && this.currentToken.value === Keywords[KeywordTypes.Return]) {
        if (this.currentToken?.matches(new Token(TokenType.Keyword, Keywords[KeywordTypes.Return]))) {
            result.registerAdvance();
            this.advance();

            const expression = result.tryRegister(this.makeExpression());
            if (!expression)
                this.reverse(result.toReverseCount)
            return result.success(new ReturnNode(expression))
        }

    }

    private makeStatements = (): ParseResult => {
        const result = new ParseResult();
        const statements = [];

        while (this.currentToken?.type === TokenType.Newline) {
            result.registerAdvance();
            this.advance();
        }

        const statement = result.register(this.makeStatement());
        if (result.error)
            return result;
        if (statement)
            statements.push(statement);

        let multipleStatements = true;

        while (true) {
            let newlineCount = 0;
            while (<TokenType>this.currentToken?.type === TokenType.Newline) {
                result.registerAdvance();
                this.advance();
                newlineCount++;
            }
            if (newlineCount)
                multipleStatements = false;
            if (!multipleStatements)
                break;
            const statement = result.tryRegister(this.makeStatement());
            if (!statement) {
                this.reverse(result.toReverseCount)
                multipleStatements = false;
                continue;
            }
            statements.push(statement);
        }
        
        return result.success(new ListNode(statements));
    }

    public parse = (tokens: Token[]) => {
        this.tokens = tokens;
        this.tokenIndex = -1;
        this.advance();
        const res = this.makeStatements();
        if (!res.error && this.currentToken?.type !== TokenType.EndOfFile)
            return res.failure(new InvalidSyntaxError('Token cannot appear after previous tokens'));
        return res;
    }

}
