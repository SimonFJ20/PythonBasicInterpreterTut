use lexer::*;
use parser::*;

mod checker;
mod codegen;
mod common;
mod lexer;
mod parser;

fn main() {
    let text = "2 + 3 + 4";
    let (tokens, token_errors) = tokenize(0, text.as_bytes());
    if token_errors.is_empty() {
        println!("tokens = ");
        for token in tokens.iter() {
            println!("\t{:?}", token.contents)
        }
    } else {
        println!("{:?}", token_errors)
    }
    let mut parser = Parser::new(0, tokens);
    let parsed = parser.parse_expression();
    if parser.errors().is_empty() {
        println!("parsed = {:#?}", parsed);
    } else {
        println!("{:?}", parser.errors());
    }
}
