
CC=clang

LFLAGS=-lm
CFLAGS=-Wall -g

all: example
	$(RM) ./*.o

example: main.o
	$(CC) -o $@ $(CFLAGS) $(LFLAGS) main.o

main.o: main.c
	$(CC) -o $@ -Wall -g -c $(CFLAGS) $<

.PHONY: clean

clean:
	$(RM) ./*.o
	$(RM) example
