
CFLAGS=-Wall -g
LFLAGS=

LD=clang
CC=gcc

TARGET=danskr

CFILES=$(wildcard *.c)
HFILES=$(wildcard *.h)
OFILES=$(patsubst %.c, %.o, $(CFILES))

$(TARGET): $(OFILES)
	$(LD) -o $@ $^ $(LFLAGS)

%.o: %.c $(HFILES)
	$(CC) -o $@ $< -c $(CFLAGS)

.PHONY: clean

clean:
	rm $(OFILES)
	rm $(TARGET)
