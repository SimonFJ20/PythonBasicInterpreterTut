
CFLAGS=-Wall

TARGET=danskr

CFILES=$(wildcard *.c)
HFILES=$(wildcard *.h)
OFILES=$(patsubst %.c, %.o, $(CFILES))

$(TARGET): $(OFILES)
	gcc -o $@ $^

%.o: %.c $(HEADERS)
	gcc -o $@ $< -c $(CFLAGS)

.PHONY: clean

clean:
	rm $(OFILES)
	rm $(TARGET)
