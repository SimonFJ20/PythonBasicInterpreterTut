
LD = gcc
CC = gcc

CFLAGS = -std=c17 -Wall -Wextra -Wpedantic -Wconversion -Wshadow

calculator: calculator.o
	$(LD) $^ -o $@

%.o: %.c
	$(cc) $< -c -o $@ $(CFLAGS)

compile_flags.txt:
	echo -xc++ $(CPP_FLAGS) | sed 's/\s\+/\n/g' > compile_flags.txt

clean:
	$(RM) *.o calculator


