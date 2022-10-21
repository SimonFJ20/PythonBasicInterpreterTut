pub const MEMORY_SIZE: usize = 16384;

pub enum Instruction {
    Mov(usize, usize),
    MovValue(usize, i8),
    Jmp(usize),
    Jnz(usize, usize),
    Not(usize),
    And(usize, usize),
    Or(usize, usize),
    Xor(usize, usize),
    Add(usize, usize),
    Sub(usize, usize),
    Mul(usize, usize),
    Div(usize, usize),
    Mod(usize, usize),
    Cmp(usize, usize),
    Lt(usize, usize),
    Gt(usize, usize),
    ShiftLeft(usize, usize),
    ShiftRight(usize, usize),
}

pub struct VM {
    pc: usize,
    ram: [i8; MEMORY_SIZE],
}

impl VM {
    pub fn new() -> Self {
        Self {
            pc: 0,
            ram: [0; MEMORY_SIZE],
        }
    }

    pub fn run_instruction(&mut self, instruction: Instruction) {
        match instruction {
            Instruction::Mov(dest, src) => {
                self.ram[dest] = self.ram[src];
            }
            Instruction::MovValue(dest, value) => {
                self.ram[dest] = value;
            }
            Instruction::Jmp(addr) => {
                self.pc = addr;
                self.pc -= 1
            }
            Instruction::Jnz(addr, cond) => {
                if self.ram[cond] != 0 {
                    self.pc = addr
                }
                self.pc -= 1
            }
            Instruction::Not(dest) => self.ram[dest] = !self.ram[dest],
            Instruction::And(dest, src) => self.ram[dest] &= self.ram[src],
            Instruction::Or(dest, src) => self.ram[dest] |= self.ram[src],
            Instruction::Xor(dest, src) => self.ram[dest] ^= self.ram[src],
            Instruction::Add(dest, src) => self.ram[dest] += self.ram[src],
            Instruction::Sub(dest, src) => self.ram[dest] -= self.ram[src],
            Instruction::Mul(dest, src) => self.ram[dest] *= self.ram[src],
            Instruction::Div(dest, src) => self.ram[dest] /= self.ram[src],
            Instruction::Mod(dest, src) => self.ram[dest] %= self.ram[src],
            Instruction::ShiftLeft(dest, src) => self.ram[dest] <<= self.ram[src],
            Instruction::ShiftRight(dest, src) => self.ram[dest] >>= self.ram[src],
            Instruction::Cmp(dest, src) => {
                self.ram[dest] = if self.ram[dest] == self.ram[src] {
                    1
                } else {
                    0
                }
            }
            Instruction::Lt(dest, src) => {
                self.ram[dest] = if self.ram[dest] < self.ram[src] { 1 } else { 0 }
            }
            Instruction::Gt(dest, src) => {
                self.ram[dest] = if self.ram[dest] > self.ram[src] { 1 } else { 0 }
            }
        }
        self.pc += 1
    }
}
