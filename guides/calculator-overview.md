
# Calculator overview

Let's try parsing `1 * 2 + (34 + 56)`.

## Lexer / Tokenizer

A token represents one or more characters.

```ts
type TokenType = string;

type Token = {
    type: TokenType,
    value: string,
};
```

![image](https://user-images.githubusercontent.com/28040410/196940996-f7872304-75f0-424c-986f-8ef3ffda5989.png)


```ts
tokens: Token[] == [
    { type: "number",   value: "1" },
    { type: "asterisk", value: "*" },
    { type: "number",   value: "2" },
    { type: "plus",     value: "+" },
    { type: "lparen",   value: "(" },
    { type: "number",   value: "34" },
    { type: "asterisk", value: "+" },
    { type: "number",   value: "56" },
    { type: "rparen",   value: ")" },
];
```

These are made using 'lexer rules':
```
/\s/    => _            /* ignore whitespace */
/\d+/   => number       /* multiple digits of integer/number */
"+"     => plus
"*"     => asterisk
"("     => lparen
")"     => rparen
```

## Parser

Turn tokens into a 'tree' of nodes, called an 'abstract syntax tree'/AST.

```ts
type Expr = { type: string };

type Number = { type: "number", value: number };

type Add =      { type: "add",      left: Expr, right: Expr };
type Multiply = { type: "multiply", left: Expr, right: Expr };
```

![image](https://user-images.githubusercontent.com/28040410/196943713-9d675b13-8cfa-4e03-8872-574e2efcc534.png)

```ts
ast: Expr == {
    type: "add",
    left: {
        type: "multiply",
        left: {
            type: "number",
            value: 1,
        },
        right: {
            type: "number",
            value: 2,
        },
    },
    right: {
        type: "add",
        left: {
            type: "number",
            value: 34,
        },
        right: {
            type: "number",
            value: 56,
        },
    },
}
```

A parser uses 'parser rules' also called a 'grammar'/'language grammar':

```
expr        ->  add

add         ->  multiply %plus% add
            |   multiply

multiply    ->  group %asterisk% multiply
            |   group

group       ->  %lparen% expr %rparen%
            |   value

value       ->  %number%
```

Shorthand functions for image below:
```ts
const add = (left: Expr, right: Expr): Add => ({ type: "add", left, right }) 
const multiply = (left: Expr, right: Expr): Multiply => ({ type: "multiply", left, right }) 
const number = (value: number): Number => ({ type: "number", value }) 
```

![image](https://user-images.githubusercontent.com/28040410/196953116-61106cd4-cdba-4cd6-962f-b9fd1aea5cf7.png)

