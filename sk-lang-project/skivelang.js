"use strict";

const fs = require("fs");

const keywords = [
    "if",
    "then",
    "else",
    "end",
    "while",
    "do",
    "fn",
    "return",
    "struct",
    "and",
    "or",
    "not",
];
const assignOperators = ["=", "+=", "-=", "*="];
const unaryOperators = ["-", "not"];
const binaryOperators = [
    "+",
    "-",
    "*",
    "/",
    "%",
    "<",
    "<=",
    ">",
    ">=",
    "==",
    "!=",
    "and",
    "or",
];
const operatorPrecedence = {
    "+": 11,
    "-": 11,
    "*": 12,
    "/": 12,
    "%": 12,
    "<": 9,
    "<=": 9,
    ">": 9,
    ">=": 9,
    "==": 8,
    "!=": 8,
    and: 4,
    or: 3,
};

class Lexer {
    /** @param {string} text */
    constructor(text) {
        this.text = text;
        this.index = 0;
        this.tokens = [];
    }

    /** @returns {string[]} */
    tokenize() {
        while (!this.done()) {
            if (this.currentMatches(/[ \n\r\t]/)) {
                this.step();
            } else if (this.currentMatches(/\d/)) {
                this.makeNumber();
            } else if (this.currentMatches(/[a-zA-Z_]/)) {
                this.makeIdentifier();
            } else {
                switch (this.current()) {
                    case '"':
                        this.makeString();
                        break;
                    case "'":
                        this.makeChar();
                        break;
                    case "+":
                        this.makePlus();
                        break;
                    case "-":
                        this.makeMinus();
                        break;
                    case "*":
                        this.makeAsterisk();
                        break;
                    case "/":
                        this.makeSlash();
                        break;
                    case "<":
                    case ">":
                        this.makeLessOrGreaterThan();
                        break;
                    case "=":
                        this.makeEqual();
                        break;
                    case "!":
                        this.makeExclamationMark();
                        break;
                    case "%":
                    case "(":
                    case ")":
                    case "[":
                    case "]":
                    case "{":
                    case "}":
                    case "<":
                    case ">":
                    case ".":
                    case ",":
                    case ":":
                    case "&":
                        this.tokens.push(this.current());
                        this.step();
                        break;
                    default:
                        throw new Error(
                            `invalid character '${this.current()}'`,
                        );
                }
            }
        }
        return this.tokens;
    }

    makeNumber() {
        let value = this.current();
        this.step();
        while (this.currentMatches(/\d/)) {
            value += this.current();
            this.step();
        }
        if (this.currentIs(".")) {
            this.step();
            if (this.currentMatches(/\d/)) {
                value += ".";
                while (this.currentMatches(/\d/)) {
                    value += this.current();
                    this.step();
                }
                this.tokens.push(value);
            } else {
                this.tokens.push(value);
                this.tokens.push(".");
            }
        } else {
            this.tokens.push(value);
        }
    }

    makeIdentifier() {
        let value = this.current();
        this.step();
        while (this.currentMatches(/[a-zA-Z_0-9]/)) {
            value += this.current();
            this.step();
        }
        this.tokens.push(value);
    }

    makeString() {
        let value = this.current();
        this.step();
        let escaped = false;
        while (!this.done()) {
            if (this.current() === '"' && !escaped) break;
            if (escaped) escaped = false;
            else if (this.currentIs("\\")) escaped = true;
            value += this.current();
            this.step();
        }
        if (!this.currentIs('"'))
            throw new Error(`expected '"', got '${this.current()}'`);
        value += this.current();
        this.step();
        this.tokens.push(value);
    }

    makeChar() {
        let value = this.current();
        this.step();
        if (this.done())
            throw new Error(`expected char value before end of file`);
        value += this.current();
        this.step();
        if (value === "'\\") {
            if (this.done())
                throw new Error(`expected char value before end of file`);
            value += this.current();
            this.step();
        }
        if (!this.currentIs("'"))
            throw new Error(`expected '\\'', got '${this.current()}'`);
        value += this.current();
        this.step();
        this.tokens.push(value);
    }

    makePlus() {
        let value = this.current();
        this.step();
        if (this.currentIs("=")) {
            value += this.current();
            this.step();
        }
        this.tokens.push(value);
    }

    makeMinus() {
        let value = this.current();
        this.step();
        if (this.currentIs("=")) {
            value += this.current();
            this.step();
        } else if (this.currentIs(">")) {
            value += this.current();
            this.step();
        }
        this.tokens.push(value);
    }

    makeAsterisk() {
        let value = this.current();
        this.step();
        if (this.currentIs("=")) {
            value += this.current();
            this.step();
        }
        this.tokens.push(value);
    }

    makeSlash() {
        let value = this.current();
        this.step();
        if (this.currentIs("/")) {
            this.step();
            while (!this.done() && this.current() !== "\n") {
                if (this.current() === "\n") {
                    this.step();
                    break;
                }
                this.step();
            }
        } else if (this.currentIs("*")) {
            this.step();
            let lastWasAsterisk = false;
            while (!this.done() && !(lastWasAsterisk && this.currentIs("/"))) {
                if (this.currentIs("*")) lastWasAsterisk = true;
                else lastWasAsterisk = false;
                this.step();
            }
            if (this.done())
                throw new Error(`expected '*/' before end of file`);
            this.step();
        } else {
            this.tokens.push(value);
        }
    }

    makeLessOrGreaterThan() {
        let value = this.current();
        this.step();
        if (this.currentIs("=")) {
            value += this.current();
            this.step();
        }
        this.tokens.push(value);
    }

    makeEqual() {
        let value = this.current();
        this.step();
        if (this.currentIs("=")) {
            value += this.current();
            this.step();
        }
        this.tokens.push(value);
    }

    makeExclamationMark() {
        let value = this.current();
        this.step();
        if (this.currentIs("=")) {
            value += this.current();
            this.step();
        }
        this.tokens.push(value);
    }

    step() {
        this.index++;
    }

    /** @returns {string} */
    current() {
        return this.text[this.index];
    }

    /** @returns {boolean} */
    done() {
        return this.index >= this.text.length;
    }

    /** @param {string} char @returns {boolean} */
    currentIs(char) {
        return !this.done() && this.current() === char;
    }

    /** @param {RegExp} regex @returns {boolean} */
    currentMatches(regex) {
        return !this.done() && regex.test(this.current());
    }
}

class Parser {
    /** @param {string[]} tokens */
    constructor(tokens) {
        this.tokens = tokens;
        this.index = 0;
    }

    parseStatements() {
        let statements = [];
        while (!this.done() && !["end", "else"].includes(this.current())) {
            statements.push(this.parseStatement());
        }
        return statements;
    }

    parseStatement() {
        switch (this.current()) {
            case "struct":
                return this.parseStruct();
            case "fn":
                return this.parseFunc();
            case "return":
                return this.parseReturn();
            case "if":
                return this.parseIf();
            case "while":
                return this.parseWhile();
            case "let":
                return this.parseLet();
        }
        const res = this.tryParseAssign();
        if (res.completed) return res.statement;
        else return { id: "expression", value: res.expression };
    }

    parseStruct() {
        this.step();
        if (this.done() || !/[a-zA-Z_][a-zA-Z_0-9]*/.test(this.current()))
            throw new Error(`expected identifier, got ${this.current()}`);
        const identifier = this.current();
        this.step();
        let fields = [];
        if (!this.done() && /[a-zA-Z_][a-zA-Z_0-9]*/.test(this.current())) {
            fields.push(this.parseParameter());
            while (!this.done() && this.current() === ",") {
                this.step();
                if (!this.done() && this.current() === "end") break;
                fields.push(this.parseParameter());
            }
        }
        if (this.done() || this.current() !== "end")
            throw new Error(`expected 'end', got '${this.current()}'`);
        this.step();
        return { id: "struct", identifier, fields };
    }

    parseFunc() {
        this.step();
        if (this.done() || !/[a-zA-Z_][a-zA-Z_0-9]*/.test(this.current()))
            throw new Error(`expected identifier, got ${this.current()}`);
        const identifier = this.current();
        this.step();
        const params = this.parseParameters();
        const type = this.parseReturnType();
        const body = this.parseStatements();
        if (this.done() || this.current() !== "end")
            throw new Error(`expected 'end', got '${this.current()}'`);
        this.step();
        return { id: "func", identifier, params, type, body };
    }

    parseReturn() {
        this.step();
        const value = this.parseExpression();
        return { id: "return", value };
    }

    parseIf() {
        this.step();
        const condition = this.parseExpression();
        if (this.done() || this.current() !== "then")
            throw new Error(`expected 'then', got '${this.current()}'`);
        this.step();
        const truthy = this.parseStatements();
        if (!this.done() && this.current() === "end") {
            this.step();
            return { id: "if", condition, truthy, falsy: null };
        } else if (!this.done() && this.current() === "else") {
            this.step();
            const falsy = this.parseStatements();
            if (this.done() || this.current() !== "end")
                throw new Error(`expected 'end', got '${this.current()}'`);
            this.step();
            return { id: "if", condition, truthy, falsy };
        } else {
            throw new Error(
                `expected 'else' or 'end', got '${this.current()}'`,
            );
        }
    }

    parseWhile() {
        this.step();
        const condition = this.parseExpression();
        if (this.done() || this.current() !== "do")
            throw new Error(`expected 'do', got '${this.current()}'`);
        this.step();
        const body = this.parseStatements();
        if (this.done() || this.current() !== "end")
            throw new Error(`expected 'end', got '${this.current()}'`);
        this.step();
        return { id: "while", condition, body };
    }

    parseLet() {
        this.step();
        if (!this.done() && /[a-zA-Z_][a-zA-Z_0-9]*/.test(this.current())) {
            const { identifier, type } = this.parseParameter();
            if (!this.done() && this.current() === "=") {
                this.step();
                const value = this.parseExpression();
                return { id: "let", identifier, type, value };
            } else {
                return { id: "let", identifier, type, value: null };
            }
        } else {
            throw new Error(`expected identifier, got ${this.current()}`);
        }
    }

    tryParseAssign() {
        const target = this.parseExpression();
        if (this.done() || !assignOperators.includes(this.current()))
            return { completed: false, expression: target };
        const op = this.current();
        this.step();
        const value = this.parseExpression();
        return {
            completed: true,
            statement: { id: "assign", target, value, op },
        };
    }

    parseExpression() {
        switch (this.current()) {
            case "fn":
                return this.parseClosure();
            case "if":
                return this.parseTernary();
            default:
                return this.parseBinary();
        }
    }

    parseClosure() {
        this.step();
        const capures = this.parseCaptures();
        const params = this.parseParameters();
        const type = this.parseReturnType();
        if (!this.done() && this.current() === "do") {
            this.step();
            const body = this.parseStatements();
            if (this.done() || this.current() !== "end")
                throw new Error(`expected 'end', got '${this.current()}'`);
            this.step();
            return { id: "closure", capures, params, type, value: null, body };
        } else if (!this.done() && this.current() === "=>") {
            this.step();
            const value = this.parseExpression();
            return { id: "closure", capures, params, type, value, body: null };
        } else {
            throw new Error(`expected 'do' or '=>', got '${this.current()}'`);
        }
    }

    parseCaptures() {
        if (this.done() || this.current() !== "[") return null;
        this.step();
        let captures = [];
        if (!this.done() && /[a-zA-Z_][a-zA-Z_0-9]*/.test(this.current())) {
            captures.push(this.current());
            this.step();
            while (!this.done() && this.current() === ",") {
                this.step();
                if (!this.done() && this.current() === "]") break;
                captures.push(this.current());
                this.step();
            }
        }
        if (this.done() || this.current() !== "]")
            throw new Error(`expected ']', got '${this.current()}'`);
        this.step();
        return captures;
    }

    parseTernary() {
        this.step();
        const condition = this.parseExpression();
        if (this.done() || this.current() !== "then")
            throw new Error(`expected 'then', got '${this.current()}'`);
        this.step();
        const truthy = this.parseExpression();
        if (this.done() || this.current() !== "else")
            throw new Error(`expected 'else', got '${this.current()}'`);
        this.step();
        const falsy = this.parseExpression();
        return { id: "ternary", condition, truthy, falsy };
    }

    parseBinary() {
        let exprs = [this.parseUnary()];
        let ops = [];
        let lastPrec = 20;
        while (!this.done()) {
            const op = this.current();
            if (!binaryOperators.includes(op)) break;
            this.step();
            const prec = operatorPrecedence[op];
            const right = this.parseUnary();
            while (prec <= lastPrec && exprs.length > 1) {
                const right = exprs.pop();
                const op = ops.pop();
                lastPrec = operatorPrecedence[op];
                if (lastPrec < prec) {
                    exprs.push(right);
                    ops.push(op);
                    break;
                }
                const left = exprs.pop();
                exprs.push({ id: "binary", left, right, op });
            }
            exprs.push(right);
            ops.push(op);
        }
        while (exprs.length > 1) {
            const right = exprs.pop();
            const left = exprs.pop();
            const op = ops.pop();
            exprs.push({ id: "binary", left, right, op });
        }
        return exprs[0];
    }

    parseUnary() {
        if (!this.done() && unaryOperators.includes(this.current())) {
            const op = this.current();
            this.step();
            return { id: "unary", value: this.parseUnary(), op };
        } else {
            return this.tryParseMemberCallIndex();
        }
    }

    tryParseMemberCallIndex() {
        let value = this.parseValue();
        while (!this.done()) {
            if (!this.done() && this.current() === ".") {
                this.step();
                if (
                    this.done() ||
                    !/[a-zA-Z_][a-zA-Z_0-9]*/.test(this.current())
                )
                    throw new Error(
                        `expected identifier, got ${this.current()}`,
                    );
                const identifier = this.current();
                this.step();
                value = { id: "member", value, identifier };
            } else if (!this.done() && this.current() === "(") {
                this.step();
                let args = [];
                if (!this.done() && this.current() !== ")") {
                    args.push(this.parseExpression());
                    while (!this.done() && this.current() === ",") {
                        this.step();
                        if (!this.done() && this.current() === ")") break;
                        args.push(this.parseExpression());
                    }
                }
                if (this.done() || this.current() !== ")")
                    throw new Error(`expected ')', got '${this.current()}'`);
                this.step();
                value = { id: "call", value, args };
            } else if (!this.done() && this.current() === "[") {
                this.step();
                const index = this.parseExpression();
                if (this.done() || this.current() !== "]")
                    throw new Error(`expected ']', got '${this.current()}'`);
                this.step();
                value = { id: "index", value, index };
            } else {
                break;
            }
        }
        return value;
    }

    parseGroup() {
        if (!this.done() && this.current() === "(") {
            this.step();
            const expression = this.parseExpression();
            if (!this.done() && this.current() !== ")")
                throw new Error(`expected ')', got '${this.current()}'`);
            this.step();
            return expression;
        } else {
            return this.parseValue();
        }
    }

    parseValue() {
        const saveValueStepReturn = (id) => {
            const value = this.current();
            this.step();
            return { id, value };
        };
        if (!this.done() && /^0x\d+$/.test(this.current())) {
            return saveValueStepReturn("hex");
        } else if (!this.done() && /^\d+$/.test(this.current())) {
            let value = this.current();
            this.step();
            if (!this.done() && this.current() === ".") {
                value += this.current();
                this.step();
                if (!this.done() && /^\d+$/.test(this.current())) {
                    value += this.current();
                    this.step();
                    return { id: "float", value };
                } else {
                    return { id: "float", value };
                }
            } else {
                return { id: "int", value };
            }
        } else if (!this.done() && /^'\\?.'$/.test(this.current())) {
            return saveValueStepReturn("char");
        } else if (!this.done() && /^".*?"$/.test(this.current())) {
            return saveValueStepReturn("string");
        } else if (
            !this.done() &&
            /[a-zA-Z_][a-zA-Z_0-9]*/.test(this.current())
        ) {
            const value = this.current();
            if (keywords.includes(value))
                throw new Error(
                    `cannot use keyword '${this.current()}' as variable name`,
                );
            this.step();
            return { id: "identifier", value };
        } else {
            throw new Error(`expected value, got '${this.current()}'`);
        }
    }

    parseParameters() {
        if (this.done() || this.current() !== "(")
            throw new Error(`expected '(', got '${this.current()}'`);
        this.step();
        let params = [];
        if (!this.done() && /[a-zA-Z_][a-zA-Z_0-9]*/.test(this.current())) {
            params.push(this.parseParameter());
            while (!this.done() && this.current() === ",") {
                this.step();
                if (!this.done() && this.current() === ")") break;
                params.push(this.parseParameter());
            }
        }
        if (this.done() || this.current() !== ")")
            throw new Error(`expected ')', got '${this.current()}'`);
        this.step();
        return params;
    }

    parseParameter() {
        if (this.done() || !/[a-zA-Z_][a-zA-Z_0-9]*/.test(this.current()))
            throw new Error(`expected identifier, got ${this.current()}`);
        const identifier = this.current();
        this.step();
        if (!this.done() && this.current() === ":") {
            this.step();
            const type = this.parseType();
            return { identifier, type };
        } else {
            return { identifier, type: null };
        }
    }

    parseReturnType() {
        if (!this.done() && ["->", ":"].includes(this.current())) {
            this.step();
            return this.parseType();
        } else {
            return null;
        }
    }

    parseType() {
        if (this.done() || !/[a-zA-Z_][a-zA-Z_0-9]*/.test(this.current()))
            throw new Error(`expected type, got ${this.current()}`);
        const value = this.current();
        this.step();
        if (!this.done() && this.current() === "<") {
            this.step();
            let params = [];
            if (!this.done() && this.current() !== ">") {
                params.push(this.parseType());
                while (!this.done() && this.current() !== ">") {
                    if (this.current() !== ",")
                        throw new Error(
                            `expected ',', got '${this.current()}'`,
                        );
                    this.step();
                    if (!this.done() && this.current() !== ">") break;
                    params.push(this.parseType());
                }
            }
            if (this.done() || this.current() !== ">")
                throw new Error(`expected '>', got '${this.current()}'`);
            this.step();
            return { id: "generic", value, params };
        } else {
            return { id: "identifier", value };
        }
    }

    step() {
        this.index += 1;
    }

    current() {
        return this.tokens[this.index];
    }

    done() {
        return this.index >= this.tokens.length;
    }
}

class Transpiler {
    constructor() {
        this.code = "";
        this.structs = [];
        this.struct_names = ["Vec", "String"];
        this.funcs = [];
        this.globals = [];
        this.closure_identifiers = [];
    }

    result() {
        const main = this.code;
        this.code = "";
        this.code += '#include "lib.h"\n';

        if (this.structs.length > 0) {
            this.code += "\n// struct forward declarations\n";
            for (const struct of this.structs)
                this.code += `typedef struct ${struct.identifier} ${struct.identifier};\n`;

            this.code += "\n// struct definitions\n";
            for (const struct of this.structs) {
                this.code += `typedef struct ${struct.identifier} {\n`;
                this.code += struct.fields;
                this.code += `} ${struct.identifier};\n`;
            }
        }

        if (this.funcs.length > 0) {
            this.code += "\n// func forward declarations\n";
            for (const func of this.funcs) {
                this.code += `${func.type} ${func.identifier}(${func.params});\n`;
            }

            this.code += "\n// func definitions\n";
            for (const func of this.funcs) {
                this.code += `${func.type} ${func.identifier}(${func.params})\n`;
                this.code += "{\n";
                this.code += func.code;
                this.code += "}\n";
            }
        }

        if (this.globals.length > 0) {
            this.code += "\n// global declarations\n";
            for (const { type, identifier } of this.globals)
                this.code += `${type} ${identifier};\n`;
        }

        this.code += "\n";
        this.code += "int main(int argc, char** argv)\n";
        this.code += "{\n";
        this.code += main;
        this.code += "}\n";
        return this.code;
    }

    transpileStatements(nodes, isTopLevel = false) {
        for (const node of nodes) {
            this.transpileStatement(node, isTopLevel);
        }
    }

    transpileStatement(node, isTopLevel) {
        switch (node.id) {
            case "struct":
                this.transpileStruct(node, isTopLevel);
                break;
            case "func":
                this.transpileFunc(node, isTopLevel);
                break;
            case "return":
                this.transpileReturn(node);
                this.code += ";\n";
                break;
            case "if":
                this.transpileIf(node);
                break;
            case "while":
                this.transpileWhile(node);
                break;
            case "let":
                this.transpileLet(node, isTopLevel);
                this.code += ";\n";
                break;
            case "assign":
                this.transpileAssign(node);
                this.code += ";\n";
                break;
            case "expression":
                this.transpileExpression(node.value);
                this.code += ";\n";
                break;
            default:
                throw new Error(`'${node.id}' not implemented`);
        }
    }

    transpileStruct(node, isTopLevel) {
        if (!isTopLevel)
            throw new Error(
                "structs can only be defined at top level (might change)",
            );
        const fields = node.fields
            .map(
                ({ type, identifier }) =>
                    `${this.transpileType(type)} ${identifier};\n`,
            )
            .join("");
        this.structs.push({ identifier: node.identifier, fields });
        this.struct_names.push(node.identifier);
    }

    transpileFunc(node, isTopLevel) {
        if (!isTopLevel)
            throw new Error(
                "functions can only be defined at top level (might change)",
            );
        const params = node.params
            .map(
                ({ type, identifier }) =>
                    `${this.transpileType(type)} ${identifier}`,
            )
            .join(", ");
        const type = this.transpileType(node.type);

        const outerCode = this.code;
        this.code = "";
        this.transpileStatements(node.body);
        const code = this.code;
        this.code = outerCode;

        this.funcs.push({ identifier: node.identifier, params, type, code });
    }

    transpileReturn(node) {
        this.code += "return ";
        this.transpileExpression(node.value);
    }

    transpileIf(node) {
        this.code += "if (";
        this.transpileExpression(node.condition);
        this.code += ") {";
        this.transpileStatements(node.truthy);
        this.code += "}";
        if (node.falsy) {
            this.code += "else {";
            this.transpileStatements(node.falsy);
            this.code += "}";
        }
    }

    transpileWhile(node) {
        this.code += "while (";
        this.transpileExpression(node.condition);
        this.code += ") {";
        this.transpileStatements(node.body);
        this.code += "}";
    }

    transpileLet(node, isTopLevel) {
        if (!node.type) throw new Error("inferrence not implemented");
        const type = this.transpileType(node.type);
        if (isTopLevel) {
            this.globals.push({ identifier: node.identifier, type });
        } else {
            this.code += type;
            this.code += " ";
        }
        this.code += node.identifier;
        if (node.value) {
            this.code += " = ";
            this.transpileExpression(node.value);
        }
    }

    transpileAssign(node) {
        this.code += "(";
        this.transpileExpression(node.target);
        this.code += ` ${node.op} `;
        this.transpileExpression(node.value);
        this.code += ")";
    }

    transpileExpression(node) {
        switch (node.id) {
            case "ternary":
                return this.transpileTernary(node);
            case "closure":
                return this.transpileClosure(node);
            case "call":
                return this.transpileCall(node);
            case "index":
                return this.transpileIndex(node);
            case "binary":
                return this.transpileBinary(node);
            case "unary":
                return this.transpileUnary(node);
            case "hex":
                return this.transpileHex(node);
            case "int":
                return this.transpileInt(node);
            case "float":
                return this.transpileFloat(node);
            case "char":
                return this.transpileChar(node);
            case "string":
                return this.transpileString(node);
            case "identifier":
                return this.transpileIdentifier(node);
            default:
                throw new Error(`'${node.id}' not implemented`);
        }
    }

    transpileTernary(node) {
        this.code += "(";
        this.transpileExpression(node.condition);
        this.code += " ? ";
        this.transpileExpression(node.truthy);
        this.code += " : ";
        this.transpileExpression(node.falsy);
        this.code += ")";
    }

    transpileClosure(node) {
        throw new Error("not implemented");
    }

    transpileCall(node) {
        if (node.value.id === "member") {
            this.code += node.value.identifier;
            this.code += "(";
            this.transpileExpression(node.value.value);
            if (node.args.length > 0) {
                this.code += ", ";
                this.transpileExpression(node.args[0]);
                for (const arg of node.args.slice(1)) {
                    this.code += ", ";
                    this.transpileExpression(arg);
                }
            }
            this.code += ")";
        } else {
            this.transpileExpression(node.value);
            this.code += "(";
            if (node.args.length > 0) {
                this.transpileExpression(node.args[0]);
                for (const arg of node.args.slice(1)) {
                    this.code += ", ";
                    this.transpileExpression(arg);
                }
            }
            this.code += ")";
        }
    }

    transpileIndex(node) {
        this.code += "vec_get(";
        this.transpileExpression(node.value);
        this.code += ", ";
        this.transpileExpression(node.index);
        this.code += ")";
    }

    transpileIndex(node) {
        this.code += "vec_get(";
        this.transpileExpression(node.value);
        this.code += ", ";
        this.transpileExpression(node.index);
        this.code += ")";
    }

    transpileBinary(node) {
        this.code += "(";
        this.transpileExpression(node.left);
        switch (node.op) {
            case "+":
            case "-":
            case "*":
            case "/":
            case "%":
            case "<":
            case ">":
            case "<=":
            case ">=":
            case "==":
            case "!=":
                this.code += ` ${node.op} `;
                break;
            case "and":
                this.code += " && ";
                break;
            case "or":
                this.code += " || ";
                break;
            default:
                throw new Error(`'${node.op}' not implemented`);
        }
        this.transpileExpression(node.right);
        this.code += ")";
    }

    transpileUnary(node) {
        this.code += "(";
        switch (node.op) {
            case "not":
                this.code += "!";
                break;
            default:
                throw new Error(`'${node.op}' not implemented`);
        }
        this.transpileExpression(node.value);
        this.code += ")";
    }

    transpileHex(node) {
        this.code += parseInt(node.value, 16).toString();
    }

    transpileInt(node) {
        this.code += parseInt(node.value).toString();
    }

    transpileFloat(node) {
        this.code += parseFloat(node.value + "0").toString();
    }

    transpileChar(node) {
        this.code += `${node.value}`;
    }

    transpileString(node) {
        this.code += `vec_from_string(${node.value})`;
    }

    transpileIdentifier(node) {
        this.code += node.value;
    }

    /** @returns {string} */
    transpileType(node) {
        if (node === null) return "void*";
        switch (node.id) {
            case "generic":
                if (this.struct_names.includes(node.value)) {
                    return `${node.value}*`;
                } else if (["Own", "Ref"].includes(node.value)) {
                    if (node.params.length < 1)
                        throw new Error("not enough generic params");
                    return this.transpileType(node.params[0]);
                } else {
                    throw new Error(`'${node.id}' not implemented`);
                }
            case "identifier":
                if (this.struct_names.includes(node.value))
                    return `${node.value}*`;
                else return node.value;
            default:
                throw new Error(`'${node.id}' not implemented`);
        }
    }
}

function transpile(ast) {
    const transpiler = new Transpiler();
    transpiler.transpileStatements(ast, true);
    return transpiler.result();
}

if (process.argv.length <= 2)
    throw new Error("not enough args; USAGE: node main.js <filename>");
const filename = process.argv[2];

const isDebug = process.argv.includes("--debug");
const printIfDebug = (...args) => {
    if (isDebug) console.log(...args);
};

const text = fs.readFileSync(filename).toString();
printIfDebug("text:\t", text);

// const tokens = tokenize(text);
const tokens = new Lexer(text).tokenize();
const tokenMaxPrintLength = 80;
printIfDebug(
    "tokens:\t",
    tokens
        .slice(1)
        .reduce(
            (acc, token) =>
                acc +
                (acc.includes("\n")
                    ? acc.length - acc.lastIndexOf("\n") >= tokenMaxPrintLength
                        ? "\n"
                        : "  "
                    : acc.length >= tokenMaxPrintLength
                    ? "\n"
                    : "  ") +
                token,
            tokens[0],
        ),
);
if (process.argv.includes("--test-tokenizer")) {
    console.log(tokens.join("\n"));
    process.exit(0);
}

const ast = new Parser(tokens).parseStatements();
printIfDebug("ast:\t", JSON.stringify(ast, null, "|   "));

const code = transpile(ast);
printIfDebug("code:\t", code);

fs.writeFileSync("out.c", code);
