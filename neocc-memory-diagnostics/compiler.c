#include "compiler.h"
#include "parser.h"
#include "utils.h"
#include <assert.h>
#include <stdlib.h>

Compiler* new_compiler(List* ast)
{
    static_assert(sizeof(Compiler) == 32, "incomplete construction of Compiler");
    Compiler* self = calloc(1, sizeof(Compiler));
    *self = (Compiler) {
        .ast = ast,
        .assembly = new_string_builder(),
        .inside_function = false,
        .current_function_name = NULL,
    };
    return self;
}

void delete_compiler(Compiler* self)
{
    delete_string_builder(self->assembly);
    free(self);
}

char* compiler_compile(Compiler* self)
{
    string_builder_write(self->assembly, ".global _start\n");
    string_builder_write(self->assembly, ".text\n");
    string_builder_write(self->assembly, "_start:\n");
    string_builder_write(self->assembly, "    call main\n");
    string_builder_write(self->assembly, "    jmp end\n");
    compiler_make_statements(self, self->ast);
    string_builder_write(self->assembly, "end:\n");
    string_builder_write(self->assembly, "    mov %rax, %rbx\n");
    string_builder_write(self->assembly, "    mov $1, %rax\n");
    string_builder_write(self->assembly, "    int $0x80\n");

    return string_builder_c_string(self->assembly);
}

void compiler_make_statements(Compiler* self, List* statements)
{
    for (int i = 0; i < statements->length(statements); i++)
        compiler_make_statement(self, statements->get(statements, i));
}

void compiler_make_statement(Compiler* self, StatementNode* node)
{
    switch (node->node_type) {
    case STATEMENT_TYPE_FUNC_DEF:
        return compiler_make_function_definition(self, (FuncDefNode*) node);
    case STATEMENT_TYPE_RETURN:
        return compiler_make_return(self, (ReturnNode*) node);
    case STATEMENT_TYPE_EXPRESSION:
    default:
        assert(!"unexpected StatementNodeType");
    }
}

void compiler_make_function_definition(Compiler* self, FuncDefNode* node)
{
    char* name = chars_to_string(node->target->value, node->target->length);

    self->inside_function = true;
    self->current_function_name = name;

    string_builder_write(self->assembly, name);
    string_builder_write(self->assembly, ":\n");
    string_builder_write(self->assembly, "    pushq %rbp\n");
    string_builder_write(self->assembly, "    movq %rsp, %rbp\n");
    compiler_make_statements(self, node->body);
    string_builder_write_fmt(self->assembly, ".%s_end:\n", name);
    string_builder_write(self->assembly, "    popq %rbp\n");
    string_builder_write(self->assembly, "    ret\n");

    self->inside_function = false;
    self->current_function_name = NULL;
    
    free(name);
}

void compiler_make_return(Compiler* self, ReturnNode* node)
{
    assert(self->inside_function);
    compiler_make_expression(self, node->value);
    string_builder_write_fmt(self->assembly, "    jmp .%s_end\n", self->current_function_name);
}

void compiler_make_expression(Compiler* self, ExpressionNode* node)
{
    switch (node->node_type) {
    case EXPRESSION_TYPE_INT:
        return compiler_make_int_literal(self, (IntNode*) node);
    default:
        assert(!"unexpected ExpressionNodeType");
    }
}

void compiler_make_int_literal(Compiler* self, IntNode* node)
{
    char* value_string = chars_to_string(node->token->value, node->token->length);
    int value = atoi(value_string);
    free(value_string);
    string_builder_write_fmt(self->assembly, "    movl $%d, %%eax\n", value);
}

char* compile(List* ast)
{
    Compiler* compiler = new_compiler(ast);
    char* result = compiler_compile(compiler);
    delete_compiler(compiler);
    return result;
}
