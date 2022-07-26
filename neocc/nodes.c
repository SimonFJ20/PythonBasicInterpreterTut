#include "parser.h"
#include "utils.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void delete_node_inheriter(Node* self)
{
    self->delete (self);
}

const char* statement_node_type_to_string(StatementNodeType type)
{
    switch (type) {
    case STATEMENT_TYPE_FUNC_DEF:
        return "STATEMENT_TYPE_FUNC_DEF";
    case STATEMENT_TYPE_RETURN:
        return "STATEMENT_TYPE_RETURN";
    case STATEMENT_TYPE_DECLARATION:
        return "STATEMENT_TYPE_DECLARATION";
    case STATEMENT_TYPE_EXPRESSION:
        return "STATEMENT_TYPE_EXPRESSION";
    }
    assert(0 && "unreachable");
}

const char* expression_node_type_to_string(ExpressionNodeType type)
{
    switch (type) {
    case EXPRESSION_TYPE_ASSIGNMENT:
        return "EXPRESSION_TYPE_ASSIGNMENT";
    case EXPRESSION_TYPE_BINARY_OPERATION:
        return "EXPRESSION_TYPE_BINARY_OPERATION";
    case EXPRESSION_TYPE_SYMBOL:
        return "EXPRESSION_TYPE_SYMBOL";
    case EXPRESSION_TYPE_INT:
        return "EXPRESSION_TYPE_INT";
    }
    assert(0 && "unreachable");
}

const char* type_node_type_to_string(TypeNodeType type)
{
    switch (type) {
    case TYPE_NODE_TYPE_KEYWORD:
        return "TYPE_NODE_TYPE_KEYWORD";
    }
    assert(0 && "unreachable");
}

const char* declaration_node_type_to_string(DeclarationNodeType type)
{
    switch (type) {
    case DECLARATION_TYPE_DEFAULT:
        return "DECLARATION_TYPE_DEFAULT";
    case DECLARATION_TYPE_INITIALIZATION:
        return "DECLARATION_TYPE_INITIALIZATION";
    }
    assert(!"unreachable");
}

DeclarationNode* new_declaration_node(TypeNode* value_type, Token* target)
{
    static_assert(sizeof(Node) == 16, "incomplete implementation of Node");
    static_assert(sizeof(DeclarationNode) == 40, "incomplete construction of DeclarationNode");
    DeclarationNode* self = calloc(1, sizeof(DeclarationNode));
    *self = (DeclarationNode) {
        .delete = delete_declaration_node,
        .to_string = declaration_node_to_string,
        .node_type = DECLARATION_TYPE_DEFAULT,
        .value_type = value_type,
        .target = target,
    };
    return self;
}

void delete_declaration_node(DeclarationNode* self)
{
    self->value_type->delete (self->value_type);
    delete_token(self->target);
    free(self);
}

char* declaration_node_to_string(DeclarationNode* self)
{
    const char* node_type = declaration_node_type_to_string(self->node_type);
    char* value_type = self->value_type->to_string(self->value_type);
    char* target = token_to_string(self->target);

    StringBuilder* sb = new_string_builder();
    string_builder_write_fmt(sb, "%s {value_type: %s, target: %s}", node_type, value_type, target);
    char* result = string_builder_c_string(sb);
    delete_string_builder(sb);

    free(value_type);
    free(target);

    return result;
}

char* declaration_nodes_to_string(List* declarations)
{
    StringBuilder* declarations_sb = new_string_builder();
    bool first = true;
    for (int i = 0; i < declarations->length(declarations); i++) {
        if (first)
            first = false;
        else
            string_builder_write(declarations_sb, ", ");
        DeclarationNode* node = declarations->get(declarations, i);
        char* node_str = node->to_string(node);
        string_builder_write(declarations_sb, node_str);
        free(node_str);
    }
    char* result = string_builder_c_string(declarations_sb);
    delete_string_builder(declarations_sb);
    return result;
}

FuncDefNode* new_func_def_node(
    Token* target,
    TypeNode* return_type,
    List* params,
    List* body)
{
    static_assert(sizeof(Node) == 16, "incomplete implementation of Node");
    static_assert(sizeof(StatementNode) == 24, "incomplete implementation of StatementNode");
    static_assert(sizeof(FuncDefNode) == 56, "incomplete construction of FuncDefNode");
    FuncDefNode* self = calloc(1, sizeof(FuncDefNode));
    *self = (FuncDefNode) {
        .delete = delete_func_def_node,
        .to_string = func_def_node_to_string,
        .node_type = STATEMENT_TYPE_FUNC_DEF,
        .target = target,
        .return_type = return_type,
        .params = params,
        .body = body,
    };
    return self;
}

void delete_func_def_node(FuncDefNode* self)
{
    self->return_type->delete (self->return_type);
    list_delete_all_and_self(self->params, (void (*)(void*)) delete_node_inheriter);
    list_delete_all_and_self(self->body, (void (*)(void*)) delete_node_inheriter);
    free(self);
}

char* func_def_node_to_string(FuncDefNode* self)
{
    const char* type = statement_node_type_to_string(self->node_type);
    char* target = token_to_string(self->target);
    char* return_type = self->return_type->to_string(self->return_type);
    char* params = "<unimplemented>";

    char* body = calloc(8192, sizeof(char));
    bool first = true;
    for (int i = 0; i < self->body->length(self->body); i++) {
        StatementNode* statement = self->body->get(self->body, i);
        char* str = statement->to_string(statement);
        if (!first)
            strcat(body, ", ");
        else
            first = false;
        strcat(body, str);
        free(str);
    }

    char* buffer = calloc(8192, sizeof(char));
    sprintf(buffer, "%s {target: %s, return_type: %s, params: [%s], body: [%s]}", type, target, return_type, params, body);
    buffer = realloc(buffer, strlen(buffer) * sizeof(char) + 1);

    free(target);
    free(return_type);
    free(body);

    return buffer;
}

ReturnNode* new_return_node(ExpressionNode* value)
{
    static_assert(sizeof(Node) == 16, "incomplete implementation of Node");
    static_assert(sizeof(StatementNode) == 24, "incomplete implementation of StatementNode");
    static_assert(sizeof(ReturnNode) == 32, "incomplete construction of ReturnNode");
    ReturnNode* self = calloc(1, sizeof(ReturnNode));
    *self = (ReturnNode) {
        .delete = delete_return_node,
        .to_string = return_node_to_string,
        .node_type = STATEMENT_TYPE_RETURN,
        .value = value,
    };
    return self;
}

void delete_return_node(ReturnNode* self)
{
    self->value->delete (self->value);
    free(self);
}

char* return_node_to_string(ReturnNode* self)
{
    const char* type = statement_node_type_to_string(self->node_type);
    char* value = self->value->to_string(self->value);

    char* buffer = calloc(8192, sizeof(char));
    sprintf(buffer, "%s {value: %s}", type, value);
    buffer = realloc(buffer, strlen(buffer) * sizeof(char) + 1);

    free(value);

    return buffer;
}

Initialization* new_initialization_node(TypeNode* value_type, Token* target, ExpressionNode* value)
{
    static_assert(sizeof(Node) == 16, "incomplete implementation of Node");
    static_assert(sizeof(DeclarationNode) == 40, "incomplete implementation of DeclarationNode");
    static_assert(sizeof(Initialization) == 48, "incomplete construction of Initialization");
    Initialization* self = calloc(1, sizeof(Initialization));
    *self = (Initialization) {
        .delete = delete_initialization_node,
        .to_string = initialization_node_to_string,
        .node_type = DECLARATION_TYPE_DEFAULT,
        .value_type = value_type,
        .target = target,
        .value = value,
    };
    return self;
}

void delete_initialization_node(Initialization* self)
{
    self->value_type->delete (self->value_type);
    delete_token(self->target);
    self->value->delete (self->value);
    free(self);
}

char* initialization_node_to_string(Initialization* self)
{
    const char* node_type = declaration_node_type_to_string(self->node_type);
    char* value_type = self->value_type->to_string(self->value_type);
    char* target = token_to_string(self->target);
    char* value = self->value->to_string(self->value);

    StringBuilder* sb = new_string_builder();
    string_builder_write_fmt(sb, "%s {value_type: %s, target: %s, value: %s}", node_type, value_type, target, value);
    char* result = string_builder_c_string(sb);
    delete_string_builder(sb);

    free(value_type);
    free(target);
    free(value);

    return result;
}

DeclStmtNode* new_declaration_statement_node(List* declarations)
{
    static_assert(sizeof(Node) == 16, "incomplete implementation of Node");
    static_assert(sizeof(StatementNode) == 24, "incomplete implementation of StatementNode");
    static_assert(sizeof(DeclStmtNode) == 32, "incomplete construction of DeclStmtNode");
    DeclStmtNode* self = calloc(1, sizeof(DeclStmtNode));
    *self = (DeclStmtNode) {
        .delete = delete_declaration_statement_node,
        .to_string = declaration_statement_node_to_string,
        .node_type = STATEMENT_TYPE_DECLARATION,
        .declarations = declarations,
    };
    return self;
}

void delete_declaration_statement_node(DeclStmtNode* self)
{
    list_delete_all_and_self(self->declarations, (void (*)(void*)) delete_node_inheriter);
    free(self);
}

char* declaration_statement_node_to_string(DeclStmtNode* self)
{
    const char* node_type = statement_node_type_to_string(self->node_type);
    char* declarations = declaration_nodes_to_string(self->declarations);

    StringBuilder* sb = new_string_builder();
    string_builder_write_fmt(sb, "%s {declarations: [%s]}", node_type, declarations);
    char* result = string_builder_c_string(sb);
    delete_string_builder(sb);

    free(declarations);
    return result;
}

ExprStmtNode* new_expression_statement_node(ExpressionNode* value)
{
    static_assert(sizeof(Node) == 16, "incomplete implementation of Node");
    static_assert(sizeof(StatementNode) == 24, "incomplete implementation of StatementNode");
    static_assert(sizeof(ExprStmtNode) == 32, "incomplete construction of ExprStmtNode");
    ExprStmtNode* self = calloc(1, sizeof(ExprStmtNode));
    *self = (ExprStmtNode) {
        .delete = delete_expression_statement_node,
        .to_string = expression_statement_to_string,
        .node_type = STATEMENT_TYPE_EXPRESSION,
        .value = value,
    };
    return self;
}

void delete_expression_statement_node(ExprStmtNode* self)
{
    self->value->delete (self->value);
    free(self);
}

char* expression_statement_to_string(ExprStmtNode* self)
{
    const char* type = statement_node_type_to_string(self->node_type);
    char* value = self->value->to_string(self->value);

    char* buffer = calloc(8192, sizeof(char));
    sprintf(buffer, "%s {value: %s}", type, value);
    buffer = realloc(buffer, strlen(buffer) * sizeof(char) + 1);

    free(value);

    return buffer;
}

KeywordTypeNode* new_keyword_type_node(Token* token)
{
    static_assert(sizeof(Node) == 16, "incomplete implementation of Node");
    static_assert(sizeof(TypeNode) == 24, "incomplete implementation of TypeNode");
    static_assert(sizeof(KeywordTypeNode) == 32, "incomplete construction of KeywordTypeNode");
    KeywordTypeNode* self = calloc(1, sizeof(KeywordTypeNode));
    *self = (KeywordTypeNode) {
        .delete = delete_keyword_type_node,
        .to_string = keyword_type_node_to_string,
        .node_type = TYPE_NODE_TYPE_KEYWORD,
        .token = token,
    };
    return self;
}

void delete_keyword_type_node(KeywordTypeNode* self)
{
    free(self);
}

char* keyword_type_node_to_string(KeywordTypeNode* self)
{
    const char* type = type_node_type_to_string(self->node_type);
    char* token = token_to_string(self->token);

    char* buffer = calloc(8192, sizeof(char));
    sprintf(buffer, "%s {value: %s}", type, token);
    buffer = realloc(buffer, strlen(buffer) * sizeof(char) + 1);

    free(token);

    return buffer;
}

const char* assignment_type_to_string(AssignmentType type)
{
    switch (type) {
    case ASSIGNMENT_TYPE_DEFAULT:
        return "ASSIGNMENT_TYPE_DEFAULT";
    }
    assert(!"unreachable");
}

AssignmentNode* new_assignment_node(AssignmentType asignment_type, Token* target, ExpressionNode* value)
{
    static_assert(sizeof(Node) == 16, "incomplete implementation of Node");
    static_assert(sizeof(ExpressionNode) == 24, "incomplete implementation of ExpressionNode");
    static_assert(sizeof(AssignmentNode) == 40, "incomplete construction of AssignmentNode");
    AssignmentNode* self = calloc(1, sizeof(AssignmentNode));
    *self = (AssignmentNode) {
        .delete = delete_assignment_node,
        .to_string = assignment_node_to_string,
        .node_type = EXPRESSION_TYPE_ASSIGNMENT,
        .asignment_type = asignment_type,
        .target = target,
        .value = value,
    };
    return self;
}

void delete_assignment_node(AssignmentNode* self)
{
    delete_token(self->target);
    self->value->delete (self->value);
    free(self);
}

char* assignment_node_to_string(AssignmentNode* self)
{
    const char* node_type = expression_node_type_to_string(self->node_type);
    char* target = token_to_string(self->target);
    char* value = self->value->to_string(self->value);

    StringBuilder* sb = new_string_builder();
    string_builder_write_fmt(sb, "%s {assignment_type: %s, target: %s, value: %s}", node_type, target, value);
    char* result = string_builder_c_string(sb);
    delete_string_builder(sb);

    free(target);
    free(value);
    return result;
}

const char* binary_operation_type_to_string(BinaryOperationType type)
{
    switch (type) {
    case BINARY_OPERATION_TYPE_ADD:
        return "BINARY_OPERATION_TYPE_ADD";
    }
    assert(!"unreachable");
}

BinaryOperationNode* new_binary_operation_node(BinaryOperationType operation_type, ExpressionNode* left, ExpressionNode* right)
{
    static_assert(sizeof(Node) == 16, "incomplete implementation of Node");
    static_assert(sizeof(ExpressionNode) == 24, "incomplete implementation of ExpressionNode");
    static_assert(sizeof(BinaryOperationNode) == 40, "incomplete construction of BinaryOperationNode");
    BinaryOperationNode* self = calloc(1, sizeof(BinaryOperationNode));
    *self = (BinaryOperationNode) {
        .delete = delete_binary_operation_node,
        .to_string = binary_operation_to_string,
        .node_type = EXPRESSION_TYPE_ASSIGNMENT,
        .operation_type = operation_type,
        .left = left,
        .right = right,
    };
    return self;
}

void delete_binary_operation_node(BinaryOperationNode* self)
{
    self->left->delete (self->left);
    self->right->delete (self->right);
    free(self);
}

char* binary_operation_to_string(BinaryOperationNode* self)
{
    const char* node_type = expression_node_type_to_string(self->node_type);
    const char* operation_type = binary_operation_type_to_string(self->operation_type);
    char* left = self->left->to_string(self->left);
    char* right = self->right->to_string(self->right);    

    StringBuilder* sb = new_string_builder();
    string_builder_write_fmt(sb, "%s {operation_type: %s, left: %s, right: %s}", node_type, operation_type, left, right);
    char* result = string_builder_c_string(sb);
    delete_string_builder(sb);

    free(left);
    free(right);
    return result;
}

SymbolNode* new_symbol_node(Token* token)
{
    static_assert(sizeof(Node) == 16, "incomplete implementation of Node");
    static_assert(sizeof(ExpressionNode) == 24, "incomplete implementation of ExpressionNode");
    static_assert(sizeof(SymbolNode) == 32, "incomplete construction of SymbolNode");
    SymbolNode* self = calloc(1, sizeof(SymbolNode));
    *self = (SymbolNode) {
        .delete = delete_symbol_node,
        .to_string = symbol_node_to_string,
        .node_type = EXPRESSION_TYPE_INT,
        .token = token,
    };
    return self;
}

void delete_symbol_node(SymbolNode* self)
{
    free(self);
}

char* symbol_node_to_string(SymbolNode* self)
{
    const char* type = expression_node_type_to_string(self->node_type);
    char* token = token_to_string(self->token);

    char* buffer = calloc(8192, sizeof(char));
    sprintf(buffer, "%s {token: %s}", type, token);
    buffer = realloc(buffer, strlen(buffer) * sizeof(char) + 1);

    free(token);

    return buffer;
}

IntNode* new_int_node(Token* token)
{
    static_assert(sizeof(Node) == 16, "incomplete implementation of Node");
    static_assert(sizeof(ExpressionNode) == 24, "incomplete implementation of ExpressionNode");
    static_assert(sizeof(IntNode) == 32, "incomplete construction of IntNode");
    IntNode* self = calloc(1, sizeof(IntNode));
    *self = (IntNode) {
        .delete = delete_int_node,
        .to_string = int_node_to_string,
        .node_type = EXPRESSION_TYPE_INT,
        .token = token,
    };
    return self;
}

void delete_int_node(IntNode* self)
{
    free(self);
}

char* int_node_to_string(IntNode* self)
{
    const char* type = expression_node_type_to_string(self->node_type);
    char* token = token_to_string(self->token);

    char* buffer = calloc(8192, sizeof(char));
    sprintf(buffer, "%s {token: %s}", type, token);
    buffer = realloc(buffer, strlen(buffer) * sizeof(char) + 1);

    free(token);

    return buffer;
}
