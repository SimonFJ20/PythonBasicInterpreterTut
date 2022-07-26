
OUT = euc

CFLAGS = -std=c17 -Wall -Werror
LFLAGS = 

CC = gcc
LD = gcc

OFILES = \
	main.o \
	list.o \
	linked_list.o \
	reader.o \
	lexer.o 

HEADERS = $(wildcard *.h)

$(OUT): $(OFILES)
	$(LD) -o $@ $^ $(LFLAGS) $(CFLAGS)

%.o: %.c $(HEADERS)
	$(CC) -o $@ -c $< $(CFLAGS)

.PHONY: clean
clean:
	$(RM) $(OFILES)
	$(RM) $(OUT)

