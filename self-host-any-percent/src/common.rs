#[derive(Debug, Clone)]
pub enum Error {
    LexerError(String),
    ParserError(String),
}

pub type FileId = usize;

#[derive(Debug, Clone)]
pub struct Span {
    pub file_id: FileId,
    pub start: usize,
    pub end: usize,
}

impl Span {
    pub fn new(file_id: FileId, start: usize, end: usize) -> Self {
        Self {
            file_id,
            start,
            end,
        }
    }

    pub fn contains(self, span: Span) -> bool {
        self.file_id == span.file_id && span.start >= self.start && span.end >= self.end
    }

    pub fn merge(a: &Span, b: &Span) -> Self {
        if a.file_id != b.file_id {
            panic!("file_id must match")
        }
        if a.start >= b.end {
            panic!("a must start before b ends")
        }
        Self {
            file_id: a.file_id,
            start: a.start,
            end: b.end,
        }
    }
}
