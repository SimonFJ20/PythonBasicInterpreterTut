from re import match
from brainfuck import brainfuck

def get_reg_num(rchar: str):
    return ord(rchar) - 96

def assemble(program: str):
    out = ''
    stackindex = 0
    lines = program.split('\n')
    for line in lines:
        args = line.split(' ')

        if match('^mov', args[0]):
            if len(args) < 3:
                return print('mov incomplete')
            if match('[a-f]', args[1]):

                if match('[a-f]', args[2]):
                    rmd = get_reg_num(args[1])
                    rms = get_reg_num(args[2])
                    out += '[<->-]' # reset temp
                    out += '>'*rms # goto source
                    out += '[' + '<'*rms + '+<+>' + '>'*rms + '-]' # move source to temp
                    out += '<'*rms + '<' # goto temp2
                    out += '[' + '>'*rms + '>+<' + '<'*rms + '-]' # move temp2 to source
                    out += '>' # go back
                    out += '[' + '>'*rmd + '+' + '<'*rmd + '-]' # move temp in destination

                elif match('\d+', args[2]):
                    regnum = get_reg_num(args[1])
                    out += '>'*regnum # goto destination
                    out += '[-]' # reset destination
                    out += '+'*int(args[2]) # set destination to source
                    out += '<'*regnum # go back

                elif match('\'\w\'', args[2]):
                    m = match(r"'(\w)'", args[2])
                    regnum = get_reg_num(args[1])
                    out += '>'*regnum # goto destination
                    out += '[-]' # reset destination
                    out += '+'*ord(m.group(1)) # set destination to source
                    out += '<'*regnum # go back
                
                else:
                    print('bad arg 2 on mov')

        elif match('^add', args[0]):
            if len(args) < 2:
                return print('add incomplete')
            if match('[a-f]', args[1]):
                rms = get_reg_num(args[1])
                out += '[<->-]' # reset temp
                out += '>'*rms # goto source
                out += '[' + '<'*rms + '+<+>' + '>'*rms + '-]' # move source to temp
                out += '<'*rms + '<' # goto temp2
                out += '[' + '>'*rms + '>+<' + '<'*rms + '-]' # move temp2 to source
                out += '>' # go back
                out += '[' + '>' + '+' + '<' + '-]' # add temp in acc

            elif match('\d+', args[1]):
                out += '>' # goto acc
                out += '+'*int(args[1]) # add source to acc
                out += '<' # go back

            elif match('\'\w\'', args[1]):
                m = match(r"'(\w)'", args[1])
                out += '>' # goto acc
                out += '+'*ord(m.group(1)) # add source to acc
                out += '<' # go back

            else:
                print('bad arg 2 on add')

        elif match('^sub', args[0]):
            if len(args) < 2:
                return print('sub incomplete')
            if match('[a-f]', args[1]):
                rms = get_reg_num(args[1])
                out += '[<->-]' # reset temp
                out += '>'*rms # goto source
                out += '[' + '<'*rms + '+<+>' + '>'*rms + '-]' # move source to temp
                out += '<'*rms + '<' # goto temp2
                out += '[' + '>'*rms + '>+<' + '<'*rms + '-]' # move temp2 to source
                out += '>' # go back
                out += '[' + '>' + '-' + '<' + '-]' # subtract acc by temp 

            elif match('\d+', args[1]):
                out += '>' # goto acc
                out += '-'*int(args[1]) # subtract acc by source
                out += '<' # go back

            elif match('\'\w\'', args[1]):
                m = match(r"'(\w)'", args[1])
                out += '>' # goto acc
                out += '-'*ord(m.group(1)) # subtract acc by source
                out += '<' # go back

            else:
                print('bad arg 2 on sub')
        
        elif match('^push', args[0]):
            out += '[<->-]' # reset temp
            out += '>>' # go to b
            out += '[<<+<+>>>-]' # move b to temp
            out += '<<<' # go to temp2
            out += '[>>>+<<<-]' # move temp2 to b
            out += '>' # go to temp1

        elif match('^print', args[0]):
            out += '>.<'

    return out


program = '''
mov a 161
sub 55
print



mov a 10
print
'''

bf = assemble(program)

print(bf)
print('Running brainfuck')
brainfuck([0]*512, 256, bf)


