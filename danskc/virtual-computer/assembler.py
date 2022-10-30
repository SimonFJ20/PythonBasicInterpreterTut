from enum import Enum, auto
from typing import Callable, Dict, List, Optional
from assembler.parser import Line, parse_lines



def assemble(text: str) -> str:
    lines = parse_lines(text)
    return "[\n" + ",".join([" ".join(line.to_json().split()) for line in lines]) + "\n]"

if __name__ == "__main__":
    from argparse import ArgumentParser
    import sys
    argparser = ArgumentParser()
    argparser.add_argument("file")
    args = argparser.parse_args()
    with open(args.file) as file:
        # print(assemble(file.read()), end="", flush=True)
        print(assemble(file.read()))
    
