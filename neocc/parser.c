#include "parser.h"
#include "utils.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

Parser* new_parser(List* tokens)
{
    Parser* self = calloc(1, sizeof(Parser));
    *self = (Parser) {
        .tokens = tokens,
        .index = 0,
        .t = tokens->get(tokens, 0),
        .done = false,
    };
    return self;
}

void delete_parser(Parser* self)
{
    free(self);
}

List* parser_parse(Parser* self)
{
    return parser_make_statements(self);
}

List* parser_make_statements(Parser* self)
{
    List* statements = (List*) new_array_list();
    while (!self->done && self->t->type != TOKEN_TYPE_RBRACE)
        statements->add(statements, parser_make_statement(self));
    if (self->t->type == TOKEN_TYPE_RBRACE)
        parser_next(self);
    return statements;
}

StatementNode* parser_make_statement(Parser* self)
{
    StatementNode* result;
    switch (self->t->type) {
    case TOKEN_TYPE_KW_RETURN:
        result = (StatementNode*) parser_make_return(self);
        break;
    case TOKEN_TYPE_KW_VOID:
    case TOKEN_TYPE_KW_INT:
        result = parser_make_declaration_definition_or_initialization(self);
        break;
    default:
        assert(!"unexpected token type");
    }
    return result;
}

ReturnNode* parser_make_return(Parser* self)
{
    parser_next(self);
    ExpressionNode* value = parser_make_expression(self);
    check_and_skip_newline(self);
    return new_return_node(value);
}

StatementNode* parser_make_declaration_definition_or_initialization(Parser* self)
{
    TypeNode* type = parser_make_type(self);
    if (self->t->type != TOKEN_TYPE_IDENTIFIER)
        assert(!"unexpected token, expected identifier");
    Token* target = self->t;
    parser_next(self);
    if (self->t->type == TOKEN_TYPE_LPAREN)
        return (StatementNode*) parser_resume_function_definition(self, target, type);
    return (StatementNode*) parser_resume_declaration_statement(self, target, type);
}

FuncDefNode* parser_resume_function_definition(Parser* self, Token* target, TypeNode* type)
{
    parser_next(self);
    if (self->t->type != TOKEN_TYPE_RPAREN)
        assert(!"unexpected token, expected ')', parameters not implemented btw");
    parser_next(self);
    if (self->t->type != TOKEN_TYPE_LBRACE)
        assert(!"unexpected token, expected '{'");
    parser_next(self);
    List* body = parser_make_statements(self);
    return new_func_def_node(target, type, (List*) new_array_list(), body);
}

DeclStmtNode* parser_resume_declaration_statement(Parser* self, Token* target, TypeNode* type)
{
    List* declarations = (List*) new_array_list();
    if (self->t->type == TOKEN_TYPE_ASSIGN) {
        parser_next(self);
        ExpressionNode* value = parser_make_expression(self);
        declarations->add(declarations, new_initialization_node(type, target, value));
    } else {
        declarations->add(declarations, new_declaration_node(type, target));
    }
    while (self->t->type == TOKEN_TYPE_COMMA) {
        TypeNode* type = parser_make_type(self);
        Token* target = self->t;
        parser_next(self);
        if (self->t->type == TOKEN_TYPE_ASSIGN) {
            parser_next(self);
            ExpressionNode* value = parser_make_expression(self);
            declarations->add(declarations, new_initialization_node(type, target, value));
        } else {
            declarations->add(declarations, new_declaration_node(type, target));
        }
    }
    check_and_skip_newline(self);
    return new_declaration_statement_node(declarations);
}

TypeNode* parser_make_type(Parser* self)
{
    Token* token = self->t;
    parser_next(self);
    switch (token->type) {
    case TOKEN_TYPE_KW_VOID:
        return (TypeNode*) new_keyword_type_node(token);
    case TOKEN_TYPE_KW_INT:
        return (TypeNode*) new_keyword_type_node(token);
    default:
        assert(!"unexpected token type");
    }
}

ExpressionNode* parser_make_expression(Parser* self)
{
    return parser_make_addition(self);
}

ExpressionNode* parser_make_addition(Parser* self)
{
    ExpressionNode* left = parser_make_value(self);
    if (self->t->type == TOKEN_TYPE_PLUS) {
        parser_next(self);
        ExpressionNode* right = parser_make_addition(self);
        return (ExpressionNode*) new_binary_operation_node(BINARY_OPERATION_TYPE_ADD, left, right);
    }
    return left;
}

ExpressionNode* parser_make_value(Parser* self)
{
    if (self->t->type == TOKEN_TYPE_IDENTIFIER) {
        Token* token = self->t;
        parser_next(self);
        return (ExpressionNode*) new_symbol_node(token);
    } else if (self->t->type == TOKEN_TYPE_INT_LITERAL) {
        Token* token = self->t;
        parser_next(self);
        return (ExpressionNode*) new_int_node(token);
    } else {
        assert(!"unexpected token type");
    }
}

void parser_skip_newline(Parser* self)
{
    while (self->t->type == TOKEN_TYPE_EOL)
        parser_next(self);
}

void check_and_skip_newline(Parser* self)
{
    if (self->t->type != TOKEN_TYPE_EOL)
        assert(!"expected ';'");
    parser_skip_newline(self);
}

void parser_next(Parser* self)
{
    self->index++;
    self->done = self->index >= self->tokens->length(self->tokens);
    self->t = self->done ? NULL : self->tokens->get(self->tokens, self->index);
    self->done = self->t->type == TOKEN_TYPE_EOF || self->done;
}

List* parse(List* tokens)
{
    Parser* parser = new_parser(tokens);
    List* ast = parser_parse(parser);
    free(parser);
    return ast;
}
