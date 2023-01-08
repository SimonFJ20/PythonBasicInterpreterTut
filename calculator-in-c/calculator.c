#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

typedef enum {
    TT_INVALID,
    TT_INT,
    TT_PLUS,
    TT_MINUS,
    TT_ASTERISK,
    TT_SLASH,
    TT_LPAREN,
    TT_RPAREN,
    TT_EOF,
} TokenTypes;

typedef struct {
    TokenTypes type;
    int index, length;
} Token;

typedef struct {
    const char* text;
    int index, text_length;
    Token current;
    bool has_read_current;
} Lexer;

Token lexer_next(Lexer* self);

void lexer_create(Lexer* self, const char* text, int text_length)
{
    *self = (Lexer) {
        .text = text,
        .index = 0,
        .text_length = text_length,
        .current = { 0 },
        .has_read_current = false,
    };
    lexer_next(self);
}

bool is_whitespace(char c) { return c == ' ' || c == '\t' || c == '\n' || c == '\r'; }
bool is_digit(char c) { return c >= '0' && c <= '9'; }

void lexer_skip_whitespace(Lexer* self)
{
    while (self->index < self->text_length && is_whitespace(self->index[self->text]))
        self->index++;
}

Token lexer_make_int(Lexer* self)
{
    int start = self->index;
    while (self->index < self->text_length && is_digit(self->index[self->text]))
        self->index++;
    self->current = (Token) { TT_INT, start, self->index - start };
    return self->current;
}

TokenTypes char_to_token_type(char value)
{
    switch (value) {
    case '+':
        return TT_PLUS;
    case '-':
        return TT_MINUS;
    case '*':
        return TT_ASTERISK;
    case '/':
        return TT_SLASH;
    case '(':
        return TT_LPAREN;
    case ')':
        return TT_RPAREN;
    default:
        return TT_INVALID;
    }
}

Token lexer_make_punctuation(Lexer* self)
{
    TokenTypes token_type = char_to_token_type(self->text[self->index]);
    if (token_type == TT_INVALID)
        return (Token) { token_type, self->index, 0 };
    self->current = (Token) { token_type, self->index, 1 };
    self->index++;
    return self->current;
}

Token lexer_next(Lexer* self)
{
    self->has_read_current = false;
    if (self->index >= self->text_length || self->text[self->index] == '\0') {
        self->current = (Token) { TT_EOF, self->index, 0 };
        return self->current;
    } else if (is_whitespace(self->text[self->index])) {
        lexer_skip_whitespace(self);
        return lexer_next(self);
    } else if (is_digit(self->text[self->index])) {
        return lexer_make_int(self);
    } else {
        return lexer_make_punctuation(self);
    }
}

Token lexer_current(Lexer* self)
{
    if (!self->has_read_current) {
        char token_value[200] = { 0 };
        for (int i = 0; i < self->current.length; i++)
            token_value[i] = self->text[self->current.index + i];
        printf("(%d, \"%s\"), ", self->current.type, token_value);
        self->has_read_current = true;
    }
    return self->current;
}

void lexer_token_string(const Lexer* self, char* destination, Token token)
{
    for (int i = 0; i < token.length; ++i)
        destination[i] = self->text[token.index + i];
}

typedef enum {
    ET_INVALID,
    ET_INT,
    ET_NEGATE,
    ET_ADD,
    ET_SUBTRACT,
    ET_MULTIPLY,
    ET_DIVIDE,
} ExprTypes;

typedef struct {
    ExprTypes type;
} Expr;

typedef struct {
    ExprTypes type;
    int value;
} IntExpr;

typedef struct {
    ExprTypes type;
    Expr* value;
} UnaryExpr;

typedef struct {
    ExprTypes type;
    Expr* left;
    Expr* right;
} BinaryExpr;

Expr* new_invalid_expr()
{
    Expr* self = malloc(sizeof(Expr));
    *self = (Expr) { ET_INVALID };
    return self;
}

Expr* new_int_expr(int value)
{
    IntExpr* self = malloc(sizeof(IntExpr));
    *self = (IntExpr) { ET_INT, value };
    return (Expr*)self;
}

Expr* new_unary_expr(ExprTypes type, Expr* value)
{
    UnaryExpr* self = malloc(sizeof(UnaryExpr));
    *self = (UnaryExpr) { type, value };
    return (Expr*)self;
}
Expr* new_binary_expr(ExprTypes type, Expr* left, Expr* right)
{
    BinaryExpr* self = malloc(sizeof(BinaryExpr));
    *self = (BinaryExpr) { type, left, right };
    return (Expr*)self;
}

void delete_expr(Expr* self)
{
    switch (self->type) {

    case ET_INVALID:
    case ET_INT:
        free(self);
        break;
    case ET_NEGATE:
        delete_expr(((UnaryExpr*)self)->value);
        free(self);
        break;
    case ET_ADD:
    case ET_SUBTRACT:
    case ET_MULTIPLY:
    case ET_DIVIDE:
        delete_expr(((BinaryExpr*)self)->left);
        delete_expr(((BinaryExpr*)self)->right);
        free(self);
    }
}

void print_expr(Expr* self)
{
    switch (self->type) {
    case ET_INVALID:
        printf("invalid");
        break;
    case ET_INT:
        printf("%d", ((IntExpr*)self)->value);
        break;
    case ET_NEGATE:
        printf("(-");
        print_expr(((UnaryExpr*)self)->value);
        printf(")");
        break;
    case ET_ADD:
        printf("(");
        print_expr(((BinaryExpr*)self)->left);
        printf(" + ");
        print_expr(((BinaryExpr*)self)->right);
        printf(")");
        break;
    case ET_SUBTRACT:
        printf("(");
        print_expr(((BinaryExpr*)self)->left);
        printf(" - ");
        print_expr(((BinaryExpr*)self)->right);
        printf(")");
        break;
    case ET_MULTIPLY:
        printf("(");
        print_expr(((BinaryExpr*)self)->left);
        printf(" * ");
        print_expr(((BinaryExpr*)self)->right);
        printf(")");
        break;
    case ET_DIVIDE:
        printf("(");
        print_expr(((BinaryExpr*)self)->left);
        printf(" / ");
        print_expr(((BinaryExpr*)self)->right);
        printf(")");
        break;
    }
}

Expr* parse_add_or_subtract(Lexer* lexer);
Expr* parse_multiply_or_divide(Lexer* lexer);
Expr* parse_negation(Lexer* lexer);
Expr* parse_grouping(Lexer* lexer);
Expr* parse_value(Lexer* lexer);

Expr* parse_expr(Lexer* lexer)
{
    return parse_add_or_subtract(lexer);
}

Expr* parse_add_or_subtract(Lexer* lexer)
{
    Expr* left = parse_multiply_or_divide(lexer);
    Token op = lexer_current(lexer);
    if (op.type == TT_PLUS) {
        lexer_next(lexer);
        Expr* right = parse_add_or_subtract(lexer);
        return new_binary_expr(ET_ADD, left, right);
    } else if (op.type == TT_ASTERISK) {
        lexer_next(lexer);
        Expr* right = parse_add_or_subtract(lexer);
        return new_binary_expr(ET_SUBTRACT, left, right);
    } else {
        return left;
    }
}

Expr* parse_multiply_or_divide(Lexer* lexer)
{
    Expr* left = parse_negation(lexer);
    Token op = lexer_current(lexer);
    if (op.type == TT_ASTERISK) {
        lexer_next(lexer);
        Expr* right = parse_multiply_or_divide(lexer);
        return new_binary_expr(ET_MULTIPLY, left, right);
    } else if (op.type == TT_SLASH) {
        lexer_next(lexer);
        Expr* right = parse_multiply_or_divide(lexer);
        return new_binary_expr(ET_DIVIDE, left, right);
    } else {
        return left;
    }
}

Expr* parse_negation(Lexer* lexer)
{
    Token op = lexer_current(lexer);
    if (op.type == TT_PLUS) {
        lexer_next(lexer);
        Expr* value = parse_negation(lexer);
        return new_unary_expr(ET_NEGATE, parse_expr(lexer));
    } else {
        return parse_grouping(lexer);
    }
}

Expr* parse_grouping(Lexer* lexer)
{
    Token op = lexer_current(lexer);
    if (op.type == TT_LPAREN) {
        lexer_next(lexer);
        Expr* value = parse_expr(lexer);
        if (lexer_current(lexer).type != TT_RPAREN)
            return new_invalid_expr();
        lexer_next(lexer);
        return value;
    } else {
        return parse_value(lexer);
    }
}

Expr* parse_value(Lexer* lexer)
{
    Token value_token = lexer_current(lexer);
    if (value_token.type == TT_INT) {
        lexer_next(lexer);
        char value_string[128];
        lexer_token_string(lexer, value_string, value_token);
        return new_int_expr(atoi(value_string));
    } else {
        return new_invalid_expr();
    }
}

int evaluate_expr(Expr* value)
{
    switch (value->type) {
    case ET_INVALID:
        return 0;
    case ET_INT:
        return ((IntExpr*)value)->value;
    case ET_NEGATE:
        return -evaluate_expr(((UnaryExpr*)value)->value);
    case ET_ADD:
        return evaluate_expr(((BinaryExpr*)value)->left) + evaluate_expr(((BinaryExpr*)value)->right);
    case ET_SUBTRACT:
        return evaluate_expr(((BinaryExpr*)value)->left) - evaluate_expr(((BinaryExpr*)value)->right);
    case ET_MULTIPLY:
        return evaluate_expr(((BinaryExpr*)value)->left) * evaluate_expr(((BinaryExpr*)value)->right);
    case ET_DIVIDE:
        return evaluate_expr(((BinaryExpr*)value)->left) / evaluate_expr(((BinaryExpr*)value)->right);
    }
}

int main()
{
    char input[128];
    fgets(input, sizeof(input), stdin);
    printf("text = \"%s\"\n", input);
    printf("tokens = [");
    Lexer lexer;
    lexer_create(&lexer, input, sizeof(input));
    Expr* ast = parse_expr(&lexer);
    printf("]\n");
    if (ast->type == TT_INVALID) {
        printf("invalid\n");
    } else {
        printf("expr = ");
        print_expr(ast);
        int value = evaluate_expr(ast);
        printf("\nresult = %d\n", value);
    }
    delete_expr(ast);
}
