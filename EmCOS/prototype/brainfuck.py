
def get_subprogram(program, i):
    subprogram = ''
    scopes = 0
    subindex = i + 1
    while program[subindex] != ']' or scopes != 0:
        subprogram += program[subindex]
        if program[subindex] == '[':
            scopes += 1
        elif program[subindex] == ']':
            scopes -= 1
        subindex += 1
    return subprogram

def brainfuck(stack: list[int], index: int, program: str):
    i = 0
    while i < len(program):
        char = program[i]
        if char == '+':
            stack[index] += 1
            if stack[index] > 255:
                stack[index] = 0
        elif char == '-':
            stack[index] -= 1
            if stack[index] < 0:
                stack[index] = 255
        elif char == '<':
            index -= 1
        elif char == '>':
            index += 1
        elif char == '.':
            print(chr(stack[index]), end='')
        elif char == ',':
            stack[index] = ord(input()[0])
        elif char == '[':
            subprogram = get_subprogram(program, i)
            while stack[index] != 0:
                brainfuck(stack, index, subprogram)
            i += len(subprogram) + 1
        elif char == ']':
            print('Unexpected "]"')
            return
        i += 1

def bfexec(program: str):
    brainfuck([0]*512, 256, program)

