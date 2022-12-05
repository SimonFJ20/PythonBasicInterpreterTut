use crate::common::*;

#[derive(Debug, Clone)]
pub enum TokenContents {
    Int(String),
    Plus,
    LParen,
    RParen,
    EOF,
    Invalid,
}

#[derive(Debug, Clone)]
pub struct Token {
    pub contents: TokenContents,
    pub span: Span,
}

impl Token {
    pub fn new(contents: TokenContents, span: Span) -> Self {
        Self { contents, span }
    }
}

pub fn tokenize(file_id: FileId, text: &[u8]) -> (Vec<Token>, Vec<Error>) {
    use TokenContents::*;
    let index = &mut 0;
    let mut tokens: Vec<Token> = Vec::new();
    let mut errors: Vec<Error> = Vec::new();
    while *index < text.len() {
        match text[*index] {
            b'+' => tokens.push(single_char_tok(file_id, index, Plus)),
            b'(' => tokens.push(single_char_tok(file_id, index, LParen)),
            b')' => tokens.push(single_char_tok(file_id, index, RParen)),
            _ => match make_token(file_id, text, index) {
                Ok(token) => tokens.push(token),
                Err(error) => errors.push(error),
            },
        }
    }
    (tokens, errors)
}

fn single_char_tok(file_id: FileId, index: &mut usize, contents: TokenContents) -> Token {
    let start = *index;
    *index += 1;
    Token::new(contents, Span::new(file_id, start, *index))
}

fn make_token(file_id: FileId, text: &[u8], index: &mut usize) -> Result<Token, Error> {
    while text[*index].is_ascii_whitespace() {
        *index += 1;
    }
    if text[*index] == b'0' {
        let start = *index;
        *index += 1;
        if *index >= text.len() {
            *index += 1;
            Ok(Token::new(
                TokenContents::Int(String::from_utf8_lossy(&text[start..*index]).to_string()),
                Span::new(file_id, start, *index),
            ))
        } else {
            match text[*index] {
                b'x' => todo!(),
                b'o' => todo!(),
                b'b' => todo!(),
                _ => Err(Error::LexerError("cannot start literal with 0".into())),
            }
        }
    } else if text[*index].is_ascii_digit() {
        let start = *index;
        while *index < text.len() && text[*index].is_ascii_digit() {
            *index += 1;
        }
        Ok(Token::new(
            TokenContents::Int(String::from_utf8_lossy(&text[start..*index]).to_string()),
            Span::new(file_id, start, *index),
        ))
    } else {
        let start = *index;
        *index += 1;
        match text[start] {
            b'+' => Ok(Token::new(
                TokenContents::Plus,
                Span::new(file_id, start, *index),
            )),
            _ => Err(Error::LexerError(format!(
                "unexpected char '{}' == {}",
                char::from(text[*index]),
                text[*index],
            ))),
        }
    }
}
