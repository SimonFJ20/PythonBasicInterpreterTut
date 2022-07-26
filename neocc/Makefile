
EXECUTABLE = neocc

CC = gcc
LD = gcc

CFLAGS = -std=c17 -Wall -Werror
LFLAGS = 

CFILES = $(wildcard *.c)
OFILES = $(patsubst %.c, %.o, $(CFILES))
HEADERS = $(wildcard *.h)

all: $(EXECUTABLE)

run: $(EXECUTABLE)
	./neocc examples/addition.c
	$(RM) temp.o temp.s

# CFLAGS += -g # compile debug symbols
valgrind: $(EXECUTABLE)
	valgrind --tool=memcheck --track-origins=yes ./neocc examples/main.c
	$(RM) temp.o temp.s

$(EXECUTABLE): $(OFILES)
	$(LD) -o $@ $(CFLAGS) $(LFLAGS) $^

%.o: %.c $(HEADERS)
	$(CC) -c -o $@ $(CFLAGS) $<

.PHONY: clean compile_flags todos

clean:
	$(RM) $(OFILES) $(EXECUTABLE)

compile_flags:
	printf "%s\n" $(CFLAGS) > compile_flags.txt

todos:
	grep FIXME * -r
	grep TODO * -r
