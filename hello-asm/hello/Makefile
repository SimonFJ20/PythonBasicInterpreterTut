
hello: hello.o
	ld hello.o -o hello

hello.o: hello.asm
	nasm -f elf64 -o hello.o hello.asm

.PHONY: clean

clean:
	$(RM) hello
	$(RM) hello.o
