@preprocessor typescript

@{%
import moo from "https://deno.land/x/moo@0.5.1.1/index.ts";
import * as ast from './ast.ts';
import { Some, None } from './utils.ts';
const lexer = moo.compile({
    nl:         {match: /[\n;]+/, lineBreaks: true},
    ws:         /[ \t]+/,
    comment_sl: /\/\/.*?$/,
    comment_ml: {match: /\*[^*]*\*+(?:[^/*][^*]*\*+)*/, lineBreaks: true},
    float:      /\-?(?:(?:0|(?:[1-9][0-9]*))\.[0-9]+)/,
    hex:        /0x[0-9a-fA-F]+/,
    int:        /0|(?:[1-9][0-9]*)/,
    char:       {match: /'(?:[^'\\]|\\[\s\S])'/, value: s => s.slice(1, -1), lineBreaks: true},
    string:     {match: /"(?:[^"\\]|\\[\s\S])*"/, value: s => s.slice(1, -1), lineBreaks: true},
    name:       {match: /[a-zA-Z0-9_]+/, type: moo.keywords({
        keyword: ['const', 'let', 'if', 'else']
    })},
    dot:        '.',

    heavyarrow: '=>',
    thinarrow:  '->',

    lparen:     '(',
    rparen:     ')',
    lbrace:     '{',
    rbrace:     '}',
    lbracket:   '[',
    rbracket:   ']',
    comma:      ',',
    
    plus:       '+',
    minus:      '-',
    powerof:    '^^',
    multiply:   '*',
    divide:     '/',
    modulus:    '%',

    log_and:    '&&',
    log_or:     '||',

    bit_and:    '&',
    bit_or:     '|',
    bit_xor:    '^',
    bit_not:    '~',
    bit_rights: '>>>',
    bit_right:  '>>',
    bit_left:   '<<',

    cmp_e:      '==',
    cmp_ne:     '!=',
    cmp_lte:    '<=',
    cmp_gte:    '>=',
    cmp_lt:     '<',
    cmp_gt:     '>',

    log_not:    '!',

    infer:     ':=',
    assign:     '=',

    qmark:      '?',
    colon:      ':',
});
%}

@lexer lexer


statements  ->  (_ statement (_nl_ statement):*):? _
    {% v => v[0] ? [v[0][1], ...v[0][2].map((v: any) => v[1])] : [] %}

statement   ->  block                   {% id %}
            |   const_declaration       {% id %}
            |   let_declaration         {% id %}
            |   if                      {% id %}
            |   if_else                 {% id %}
            |   while                   {% id %}
            |   expression_statement    {% id %}

block       ->  "{" statements "}"
                    {% v => new ast.Block(v[1]) %}

const_declaration   ->  "const" __ argument _ "=" _ expression
                            {% v => new ast.ConstDefinition(v[2], v[6]) %}

let_declaration     ->  "let" __ argument _ ("=" _ expression):?
                            {% v => new ast.LetDeclaration(v[2], v[5] ? Some(v[5][2]) : None()) %}

if          ->  "if" _ "(" _ expression _ ")" _ statement
                    {% v => new ast.If(v[4], v[8]) %}

if_else     ->  "if" _ "(" _ expression _ ")" _ statement _ "else" _ statement
                    {% v => new ast.IfElse(v[4], v[8], v[12]) %}

while       ->  "while" _ "(" _ expression _ ")" _ statement
                    {% v => new ast.While(v[4], v[8]) %}

expression_statement    ->  expression
                                {% v => new ast.ExpressionStatement(v[0]) %}

expressions ->  (_ expression (_ "," _ expression):*):? _
                    {% v => v[0] ? [v[0][1], ...v[0][2].map((v: any) => v[3])] : [] %}

type_list   ->  (_ type (_ "," _ type):*):? _
                    {% v => v[0] ? [v[0][1], ...v[0][2].map((v: any) => v[3])] : [] %}

type_specifier  ->  ":" _ type
                        {% v => v[2] %}

type        ->  function_type   {% id %}
            |   type_literal    {% id %}

function_type   ->  "(" type_list ")" _ "=>" _ type
                        {% v => new ast.FunctionType(v[1], v[6]) %}

type_literal    ->  "int"
                            {% v => new ast.IntType() %}
                |   "string"
                            {% v => new ast.IntType() %}
                |   "void"
                            {% v => new ast.VoidType() %}

expression  ->  function        {% id %}
            |   precedence_1    {% id %}

function    ->  "(" arguments ")" _ (type_specifier _):? block
                    {% v => new ast.Function(v[1], v[4] ? Some(v[4][0]) : None(), v[5]) %}
            |   "(" arguments ")" _ (type_specifier _):? "=>" _ expression
                    {% v => new ast.Function(v[1], v[4] ? Some(v[4][0]) : None(), v[7]) %}

arguments   ->  (_ argument (_ "," _ argument):*):? _
                    {% v => v[0] ? [v[0][1], ...v[0][2].map((v: any) => v[3])] : [] %}

argument    ->  %name _ type_specifier
                    {% v => new ast.Argument(v[0].value, v[2]) %}

precedence_1    ->  precedence_2    {% id %}
precedence_2    ->  precedence_3    {% id %}
precedence_3    ->  precedence_4    {% id %}
precedence_4    ->  precedence_5    {% id %}
precedence_5    ->  precedence_6    {% id %}
precedence_6    ->  precedence_8    {% id %}
precedence_8    ->  precedence_9    {% id %}
precedence_9    ->  precedence_10   {% id %}
precedence_10   ->  precedence_11   {% id %}
precedence_11   ->  precedence_12   {% id %}

precedence_12   ->  precedence_12 _ "+" _ precedence_13
                        {% v => new ast.BinaryOperation(ast.OperationType.Add, v[0], v[4]) %}
                |   precedence_12 _ "-" _ precedence_13
                        {% v => new ast.BinaryOperation(ast.OperationType.Subtract, v[0], v[4]) %}
                |   precedence_13   {% id %}

precedence_13   ->  precedence_13 _ "*" _ precedence_14
                        {% v => new ast.BinaryOperation(ast.OperationType.Multiply, v[0], v[4]) %}
                |   precedence_13 _ "/" _ precedence_14
                        {% v => new ast.BinaryOperation(ast.OperationType.Divide, v[0], v[4]) %}
                |   precedence_13 _ "%" _ precedence_14
                        {% v => new ast.BinaryOperation(ast.OperationType.Modulus, v[0], v[4]) %}
                |   precedence_14   {% id %}

precedence_14   ->  precedence_15   {% id %}
precedence_15   ->  precedence_16   {% id %}
precedence_16   ->  precedence_17   {% id %}
precedence_17   ->  precedence_18   {% id %}

precedence_18   ->  precedence_18 _ "(" expressions ")"
                        {% v => new ast.Call(v[0], v[3]) %}
                |   precedence_19   {% id %}

precedence_19   ->  value           {% id %}

value       ->  %int
                    {% v => new ast.Int(v[0].value) %}
            |   %string
                    {% v => new ast.String(v[0].value) %}
            |   %name
                    {% v => new ast.Accessor(v[0].value) %}
            |   "(" _ expression _ ")"
                    {% v => v %} 

_           ->  __:?
__          ->  (%ws|%nl|%comment_sl|%comment_ml):+

_nl_        ->  sl_ (%nl sl_):+

sl_         ->  sl__:?
sl__        ->  (%ws|%comment_sl|%comment_ml):+
