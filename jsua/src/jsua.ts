import { Lexer } from './lexer'


export const interpret = (text: string) => {

    const lexer = new Lexer();
    return lexer.lex(text);

}
