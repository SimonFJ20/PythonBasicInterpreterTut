import {
    ignoreSingleLineWhitespaceRule,
    charPatternRule,
    tokenize,
    intRule,
    hexRule,
    identifierRule,
    ignoreMultiLineComment,
    ignoreSingleLineComment,
    charLiteralRule,
    stringLiteralRule,
    ignorePatternRule,
} from "./lexer.ts";
import { parse } from "./parser.ts";
import { TokenType } from "./tokentypes.ts";

const main = () => {
    if (Deno.args.length <= 0) throw new Error("no input file");
    const filename = Deno.args[0];
    const text = Deno.readTextFileSync(filename);

    const tokens = tokenize<TokenType>(text, [
        hexRule(TokenType.HexLiteral),
        intRule(TokenType.IntLiteral),
        charPatternRule(TokenType.LetKeyword, "let"),
        charPatternRule(TokenType.LetKeyword, "mut"),
        identifierRule(TokenType.Identifier),
        ignoreSingleLineWhitespaceRule(),
        ignoreSingleLineComment(),
        ignoreMultiLineComment(),
        charLiteralRule(TokenType.CharLiteral),
        stringLiteralRule(TokenType.StringLiteral),
        charPatternRule(TokenType.LParen, "("),
        charPatternRule(TokenType.RParen, ")"),
        charPatternRule(TokenType.LBrace, "{"),
        charPatternRule(TokenType.RBrace, "}"),
        charPatternRule(TokenType.LBracket, "["),
        charPatternRule(TokenType.RBracket, "]"),
        charPatternRule(TokenType.Equal, "="),
        charPatternRule(TokenType.Plus, "+"),
        charPatternRule(TokenType.Minus, "-"),
        charPatternRule(TokenType.Asterisk, "*"),
        charPatternRule(TokenType.Slash, "/"),
        charPatternRule(TokenType.Percentage, "%"),
        charPatternRule(TokenType.Equal, "="),
        charPatternRule(TokenType.Colon, ":"),
        // charPatternRule(TokenType.NewLine, '\r\n'),
        // charPatternRule(TokenType.NewLine, '\n'),
        // charPatternRule(TokenType.LineTerminator, ';'),
        ignorePatternRule(/^[\r\n;]/),
    ]);

    // console.log(tokens)

    const ast = parse(tokens);

    console.log(ast);
};

main();
