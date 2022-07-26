#include "compiler.h"
#include "parser.h"
#include "utils.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv)
{
    assert(argc >= 2 && "not enough args / no input file");

    char* content = read_file(argv[1]);

    List* tokens = tokenize(content);
    printf("=== TOKENIZING(TEXT) -> TOKENS ===\n");
    for (int i = 0; i < tokens->length(tokens); i++)
        println_and_free(token_to_string(tokens->get(tokens, i)));

    printf("=== PARSING(TOKENS) -> AST ===\n");
    List* ast = parse(tokens);
    for (int i = 0; i < ast->length(ast); i++) {
        StatementNode* node = (StatementNode*) ast->get(ast, i);
        println_and_free(node->to_string(node));
    }

    printf("=== COMPILING(AST) -> ASSEMBLY ===\n");
    char* assembly = compile(ast);
    printf("%s\n", assembly);

    write_file("temp.s", assembly);

    int assembler_exit_code = system("as temp.s -o temp.o --warn --fatal-warnings");
    assert(assembler_exit_code == 0);
    int linker_exit_code = system("ld temp.o -o a.out");
    assert(linker_exit_code == 0);

    free(assembly);
    list_delete_all_and_self(ast, (void (*)(void*)) delete_node_inheriter);
    list_delete_all_and_self(tokens, (void (*)(void*)) delete_token);
    free(content);
}
