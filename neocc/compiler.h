#pragma once

#include <stdbool.h>
#include "utils.h"
#include "parser.h"

typedef struct Compiler {
    List* ast;
    StringBuilder* assembly;
    bool inside_function;
    char* current_function_name;
} Compiler;

Compiler* new_compiler(List* ast);
void delete_compiler(Compiler* self);
char* compiler_compile(Compiler* self);
void compiler_make_statements(Compiler* self, List* statements);
void compiler_make_statement(Compiler* self, StatementNode* node);
void compiler_make_function_definition(Compiler* self, FuncDefNode* node);
void compiler_make_return(Compiler* self, ReturnNode* node);
void compiler_make_expression(Compiler* self, ExpressionNode* node);
void compiler_make_int_literal(Compiler* self, IntNode* node);

char* compile(List* ast);
