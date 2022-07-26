#pragma once

#include "utils.h"
#include <stdbool.h>

typedef enum TokenType {
    TOKEN_TYPE_IDENTIFIER,
    TOKEN_TYPE_KW_VOID,
    TOKEN_TYPE_KW_INT,
    TOKEN_TYPE_KW_IF,
    TOKEN_TYPE_KW_ELSE,
    TOKEN_TYPE_KW_FOR,
    TOKEN_TYPE_KW_WHILE,
    TOKEN_TYPE_KW_SWITCH,
    TOKEN_TYPE_KW_CASE,
    TOKEN_TYPE_KW_RETURN,
    TOKEN_TYPE_KW_CONTINUE,
    TOKEN_TYPE_KW_BREAK,
    TOKEN_TYPE_INT_LITERAL,
    TOKEN_TYPE_LPAREN,
    TOKEN_TYPE_RPAREN,
    TOKEN_TYPE_LBRACE,
    TOKEN_TYPE_RBRACE,
    TOKEN_TYPE_LBRACKET,
    TOKEN_TYPE_RBRACKET,
    TOKEN_TYPE_COMMA,
    TOKEN_TYPE_ASSIGN,
    TOKEN_TYPE_EQUAL,
    TOKEN_TYPE_PLUS,
    TOKEN_TYPE_EOL,
    TOKEN_TYPE_EOF,
} TokenType;

const char* token_type_to_string(TokenType type);

typedef struct Token {
    TokenType type;
    const char* value;
    size_t length;
} Token;

Token* new_token(
    const TokenType type,
    const char* value,
    const size_t length);
void delete_token(Token* self);
char* token_to_string(Token* self);

typedef struct Lexer {
    const char* text;
    int index;
    char c;
    bool done;
} Lexer;

Lexer* new_lexer(char* text);
void delete_lexer(Lexer* self);
List* lexer_tokenize(Lexer* self);
Token* lexer_match_char(Lexer* self);
Token* lexer_make_number(Lexer* self);
Token* lexer_make_name(Lexer* self);
Token* lexer_make_equal_or_assign(Lexer* self);
void lexer_next(Lexer* self);

List* tokenize(char* text);

typedef struct Node {
    void (*delete)(struct Node* self);
    char* (*to_string)(struct Node* self);
} Node;

// Should only be used as passed deletor.
void delete_node_inheriter(Node* self);

typedef enum StatementNodeType {
    STATEMENT_TYPE_FUNC_DEF,
    STATEMENT_TYPE_RETURN,
    STATEMENT_TYPE_DECLARATION,
    STATEMENT_TYPE_EXPRESSION,
} StatementNodeType;

const char* statement_node_type_to_string(StatementNodeType type);

typedef struct StatementNode {
    void (*delete)(struct StatementNode* self);
    char* (*to_string)(struct StatementNode* self);
    StatementNodeType node_type;
} StatementNode;

typedef enum ExpressionNodeType {
    EXPRESSION_TYPE_ASSIGNMENT,
    EXPRESSION_TYPE_BINARY_OPERATION,
    EXPRESSION_TYPE_SYMBOL,
    EXPRESSION_TYPE_INT,
} ExpressionNodeType;

const char* expression_node_type_to_string(ExpressionNodeType type);

typedef struct ExpressionNode {
    void (*delete)(struct ExpressionNode* self);
    char* (*to_string)(struct ExpressionNode* self);
    ExpressionNodeType node_type;
} ExpressionNode;

typedef enum TypeNodeType {
    TYPE_NODE_TYPE_KEYWORD,
} TypeNodeType;

const char* type_node_type_to_string(TypeNodeType type);

typedef struct TypeNode {
    void (*delete)(struct TypeNode* self);
    char* (*to_string)(struct TypeNode* self);
    TypeNodeType node_type;
} TypeNode;

typedef enum DeclarationNodeType {
    DECLARATION_TYPE_DEFAULT,
    DECLARATION_TYPE_INITIALIZATION,
} DeclarationNodeType;

const char* declaration_node_type_to_string(DeclarationNodeType type);

typedef struct DeclarationNode {
    void (*delete)(struct DeclarationNode* self);
    char* (*to_string)(struct DeclarationNode* self);
    DeclarationNodeType node_type;
    TypeNode* value_type;
    Token* target;
} DeclarationNode;

DeclarationNode* new_declaration_node(TypeNode* value_type, Token* target);
void delete_declaration_node(DeclarationNode* self);
char* declaration_node_to_string(DeclarationNode* self);

char* declaration_nodes_to_string(List* declarations);

typedef struct FuncDefNode {
    void (*delete)(struct FuncDefNode* self);
    char* (*to_string)(struct FuncDefNode* self);
    StatementNodeType node_type;
    Token* target;
    TypeNode* return_type;
    List* params;
    List* body;
} FuncDefNode;

FuncDefNode* new_func_def_node(
    Token* target,
    TypeNode* return_type,
    List* params,
    List* body);
void delete_func_def_node(FuncDefNode* self);
char* func_def_node_to_string(FuncDefNode* self);

typedef struct ReturnNode {
    void (*delete)(struct ReturnNode* self);
    char* (*to_string)(struct ReturnNode* self);
    StatementNodeType node_type;
    ExpressionNode* value;
} ReturnNode;

ReturnNode* new_return_node(ExpressionNode* value);
void delete_return_node(ReturnNode* self);
char* return_node_to_string(ReturnNode* self);

typedef struct Initialization {
    void (*delete)(struct Initialization* self);
    char* (*to_string)(struct Initialization* self);
    DeclarationNodeType node_type;
    TypeNode* value_type;
    Token* target;
    ExpressionNode* value;
} Initialization;

Initialization* new_initialization_node(TypeNode* value_type, Token* target, ExpressionNode* value);
void delete_initialization_node(Initialization* self);
char* initialization_node_to_string(Initialization* self);

typedef struct DeclStmtNode {
    void (*delete)(struct DeclStmtNode* self);
    char* (*to_string)(struct DeclStmtNode* self);
    StatementNodeType node_type;
    List* declarations;
} DeclStmtNode;

DeclStmtNode* new_declaration_statement_node(List* declarations);
void delete_declaration_statement_node(DeclStmtNode* self);
char* declaration_statement_node_to_string(DeclStmtNode* self);

typedef struct ExprStmtNode {
    void (*delete)(struct ExprStmtNode* self);
    char* (*to_string)(struct ExprStmtNode* self);
    StatementNodeType node_type;
    ExpressionNode* value;
} ExprStmtNode;

ExprStmtNode* new_expression_statement_node(ExpressionNode* value);
void delete_expression_statement_node(ExprStmtNode* self);
char* expression_statement_to_string(ExprStmtNode* self);

typedef struct KeywordTypeNode {
    void (*delete)(struct KeywordTypeNode* self);
    char* (*to_string)(struct KeywordTypeNode* self);
    TypeNodeType node_type;
    Token* token;
} KeywordTypeNode;

KeywordTypeNode* new_keyword_type_node(Token* token);
void delete_keyword_type_node(KeywordTypeNode* self);
char* keyword_type_node_to_string(KeywordTypeNode* self);

typedef enum AssignmentType {
    ASSIGNMENT_TYPE_DEFAULT,
} AssignmentType;

const char* assignment_type_to_string(AssignmentType type);

typedef struct AssignmentNode {
    void (*delete)(struct AssignmentNode* self);
    char* (*to_string)(struct AssignmentNode* self);
    ExpressionNodeType node_type;
    AssignmentType asignment_type;
    Token* target;
    ExpressionNode* value;
} AssignmentNode;

AssignmentNode* new_assignment_node(AssignmentType asignment_type, Token* target, ExpressionNode* value);
void delete_assignment_node(AssignmentNode* self);
char* assignment_node_to_string(AssignmentNode* self);

typedef enum BinaryOperationType {
    BINARY_OPERATION_TYPE_ADD,
} BinaryOperationType;

const char* binary_operation_type_to_string(BinaryOperationType type);

typedef struct BinaryOperationNode {
    void (*delete)(struct BinaryOperationNode* self);
    char* (*to_string)(struct BinaryOperationNode* self);
    ExpressionNodeType node_type;
    BinaryOperationType operation_type;
    ExpressionNode* left;
    ExpressionNode* right;
} BinaryOperationNode;

BinaryOperationNode* new_binary_operation_node(BinaryOperationType operation_type, ExpressionNode* left, ExpressionNode* right);
void delete_binary_operation_node(BinaryOperationNode* self);
char* binary_operation_to_string(BinaryOperationNode* self);

typedef struct SymbolNode {
    void (*delete)(struct SymbolNode* self);
    char* (*to_string)(struct SymbolNode* self);
    ExpressionNodeType node_type;
    Token* token;
} SymbolNode;

SymbolNode* new_symbol_node(Token* token);
void delete_symbol_node(SymbolNode* self);
char* symbol_node_to_string(SymbolNode* self);

typedef struct IntNode {
    void (*delete)(struct IntNode* self);
    char* (*to_string)(struct IntNode* self);
    ExpressionNodeType node_type;
    Token* token;
} IntNode;

IntNode* new_int_node(Token* token);
void delete_int_node(IntNode* self);
char* int_node_to_string(IntNode* self);

typedef struct Parser {
    List* tokens;
    int index;
    Token* t;
    bool done;
} Parser;

Parser* new_parser(List* tokens);
void delete_parser(Parser* self);
List* parser_parse(Parser* self);
void parser_next(Parser* self);
List* parser_make_statements(Parser* self);
StatementNode* parser_make_statement(Parser* self);
StatementNode* parser_make_declaration_definition_or_initialization(Parser* self);
FuncDefNode* parser_resume_function_definition(Parser* self, Token* target, TypeNode* type);
DeclStmtNode* parser_resume_declaration_statement(Parser* self, Token* target, TypeNode* type);
TypeNode* parser_make_type(Parser* self);
ReturnNode* parser_make_return(Parser* self);
ExpressionNode* parser_make_expression(Parser* self);
ExpressionNode* parser_make_addition(Parser* self);
ExpressionNode* parser_make_value(Parser* self);
void parser_skip_newline(Parser* self);
void check_and_skip_newline(Parser* self);

List* parse(List* tokens);
