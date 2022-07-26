from sys import argv
from htb_interpreter import evaluate

def run_text(text: str, filename: str, print_res: bool = True):
    try:
        result, error = evaluate(filename, text)

        if error: print(error.as_string())
        elif result and print_res:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))
    except KeyboardInterrupt:
        return None

def repl():
    while True:
        try:
            try:
                text = input('❱❱❱ ')
            except UnicodeEncodeError:
                text = input('>>> ').replace('\n', '', -1)
        except KeyboardInterrupt:
            exit()

        if text.strip() == '': continue

        run_text(text, '<stdin>')

if __name__ == '__main__':
    if len(argv) < 2:
        repl()
    else:
        filepath = argv[1]
        with open(filepath, 'r') as file:
            text = file.read()
            file.close()
        if text.strip() == '':
            print(f"Empty file '{filepath}'")
            exit(1)
        print_res = '-s' in argv or '--status' in argv
        run_text(text, filepath, print_res)
