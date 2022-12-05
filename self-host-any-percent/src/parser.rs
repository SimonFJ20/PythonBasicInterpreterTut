use crate::{common::*, lexer::*};

#[derive(Debug)]
pub enum ParsedExpression {
    Expression(Box<ParsedExpression>, Span),
    Add(Box<ParsedExpression>, Box<ParsedExpression>, Span),
    Int(String, Span),
    Invalid(Error, Span),
}

impl ParsedExpression {
    pub fn span(&self) -> &Span {
        match self {
            ParsedExpression::Expression(_, span) => span,
            ParsedExpression::Add(_, _, span) => span,
            ParsedExpression::Int(_, span) => span,
            ParsedExpression::Invalid(_, span) => span,
        }
    }
}

pub struct Parser {
    file_id: FileId,
    tokens: Vec<Token>,
    errors: Vec<Error>,
    index: usize,
}

impl Parser {
    pub fn new(file_id: FileId, tokens: Vec<Token>) -> Self {
        Self {
            file_id,
            tokens,
            errors: Vec::new(),
            index: 0,
        }
    }

    pub fn errors(&self) -> Vec<Error> {
        self.errors.clone()
    }

    pub fn parse_expression(&mut self) -> ParsedExpression {
        self.parse_prec_11()
    }

    pub fn parse_prec_11(&mut self) -> ParsedExpression {
        let left = self.parse_value();
        if self.index >= self.tokens.len() {
            return left;
        }
        let operator = self.tokens[self.index].clone();
        match operator.contents {
            TokenContents::Plus => {
                self.index += 1;
                let right = self.parse_prec_11();
                let span = Span::merge(left.span(), right.span());
                ParsedExpression::Add(Box::new(left), Box::new(right), span)
            }
            _ => left,
        }
    }

    pub fn parse_value(&mut self) -> ParsedExpression {
        let token = self.tokens[self.index].clone();
        self.index += 1;
        match token.contents {
            TokenContents::Int(value) => ParsedExpression::Int(value, token.span),
            TokenContents::LParen => {
                let expr = self.parse_expression();
                match self.tokens[self.index].contents {
                    TokenContents::RParen => {
                        let rparen = self.tokens[self.index].clone();
                        self.index += 1;
                        ParsedExpression::Expression(
                            Box::new(expr),
                            Span::merge(&token.span, &rparen.span),
                        )
                    }
                    _ => ParsedExpression::Invalid(
                        Error::ParserError("unexpected token".into()),
                        Span::merge(&token.span, &self.tokens[self.index].span),
                    ),
                }
            }
            _ => {
                ParsedExpression::Invalid(Error::ParserError("unexpected token".into()), token.span)
            }
        }
    }
}
