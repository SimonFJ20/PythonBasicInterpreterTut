use std::collections::HashMap;

struct Object {
    next_link_node: Option<Box<Object>>,
    gc_marked: bool,
    properties: HashMap<String, Object>,
}

enum Instruction {
    Jump(usize),
}

fn main() {
    println!("Hello, world!");
}
