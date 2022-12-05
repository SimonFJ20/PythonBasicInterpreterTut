use crate::{common::*, parser::*};

pub enum Type {
    I32,
}

pub enum CheckedExpression {
    Expression(Box<CheckedExpression>, Type, Span),
    Add(Box<CheckedExpression>, Box<CheckedExpression>, Type, Span),
    Int(String, Type, Span),
}

pub struct Checker {
    errors: Vec<Error>,
}

impl Checker {
    pub fn new() -> Self {
        Self { errors: Vec::new() }
    }

    pub fn errors(&self) -> Vec<Error> {
        self.errors.clone()
    }

    pub fn check(ast: ParsedExpression) -> Result<CheckedExpression, Vec<Error>> {
        todo!()
    }
}
