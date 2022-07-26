
#
# Makefile by SimonFJ20
#

BIN=out

CC=gcc

LFLAGS=-lm
CFLAGS=-g -Wall

SRC=src
HDR=src
OBJ=obj
LIB=lib

SRCS=$(wildcard $(SRC)/*.c)
HDRS=$(wildcard $(HDR)/*.h)
OBJS=$(patsubst $(SRC)/%.c, $(OBJ)/%.o, $(SRCS))

$(BIN): $(OBJS) $(OBJ)
	$(CC) $(OBJS) -o $@ -L$(LIB) $(CFLAGS) $(LFLAGS)

$(OBJ)/%.o: $(SRC)/%.c $(OBJ) $(HDRS)
	$(CC) -c $< -o $@ -I$(HDR) $(CFLAGS)

$(OBJ):
	mkdir -p $@

.PHONY: clean

clean:
	$(RM) -r $(OBJ)
	$(RM) $(BIN)

