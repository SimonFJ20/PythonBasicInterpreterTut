use std::collections::HashMap;

enum ObjectValue {
    Null,
    Int(i64),
    Float(f64),
    String(String),
    List(Vec<Object>),
    Dict(HashMap<String, Object>),
    Clojure(HashMap<String, Object>, usize),
}

struct Object {
    next_link_node: Option<Box<Object>>,
    gc_marked: bool,
    value: ObjectValue,
}

impl Object {
    pub fn new(value: ObjectValue) -> Self {
        Self {
            gc_marked: false,
            next_link_node: None,
            value,
        }
    }
}

enum Instruction {
    Jump(usize),
    LoadReg(usize),
    StoreReg(usize),
    Push(Object),
    Pop,
}

struct VM {
    program: Vec<Instruction>,
    stack: Vec<Object>,
    registers: HashMap<usize, Object>,
}

impl VM {
    pub fn new(program: Vec<Instruction>) -> Self {
        Self {
            program,
            stack: Vec::new(),
            registers: HashMap::new(),
        }
    }
}

fn main() {
    println!("Hello, world!");
}
