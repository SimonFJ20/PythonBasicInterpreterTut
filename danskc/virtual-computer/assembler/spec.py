
PROGRAM_START = 64

def instruction_size(operator: str) -> int:
    if operator == "noop":
        return 1
    elif operator in ["jmp"]:
        return 2
    elif operator in ["jnz", "mov", "and", "or", "xor", "add", "sub", "mul", "div", "mod", "shl", "cmp", "lt", "load", "store"]:
        return 3
    else:
        raise Exception(f"unknown instruction \"{operator}\"")
